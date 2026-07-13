
// ── Navegação entre telas - alterna qual das .screen está visivel.
function showScreen(id){
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));    // Seleciona as três telas, e remove a classe active de cada um, escondendo-as
  document.getElementById("screen-" + id).classList.add("active");
}

document.getElementById("btn-modalidades").addEventListener("click", () => showScreen("modalidades"));

document.querySelectorAll("[data-destino]").forEach(btn => {
  btn.addEventListener("click", () => showScreen(btn.getAttribute("data-destino")));
});

// ── Botão SAIR ────────────────────────────────────────────
const shutdownOverlay = document.getElementById("shutdown-overlay");
document.getElementById("btn-sair").addEventListener("click", () => shutdownOverlay.classList.add("active"));
document.getElementById("btn-reconectar").addEventListener("click", () => shutdownOverlay.classList.remove("active"));

// ── Seleção de modalidade ─────────────────────────────────
document.querySelectorAll(".mod-card").forEach(card => {
  card.addEventListener("click", () => abrirChat(card.getAttribute("data-modalidade")));
});

// ── Estado local do front end ─────────────────────────────
let turnoAtual        = "investigador";
let ultimaPerguntaInv = "";   // texto da pergunta atual do Investigador
let ultimaPerguntaResp= "";   // texto da pergunta atual do Respondedor
let aguardandoChute   = null; // "investigador" | "respondedor" | null

// ── Abrir chat e iniciar partida ──────────────────────────
async function abrirChat(modalidadeId){
  document.getElementById("chat-title").textContent = modalidadeId === "1" ? "ANIMAIS" : "FRUTAS";
  document.getElementById("chat-ref").textContent   = "REF: MOD-0" + modalidadeId;

  document.getElementById("log-investigador").innerHTML = "";
  document.getElementById("log-respondedor").innerHTML  = "";

  turnoAtual         = "investigador";
  ultimaPerguntaInv  = "";
  ultimaPerguntaResp = "";
  aguardandoChute    = null;

  showScreen("chat");

  // Inicia partida no backend
  try {
    const res = await fetch("/api/jogo/iniciar", { method: "POST" });
    const data = await res.json();
    addMsg("log-investigador", "system", "SISTEMA", "Pense em um animal e responda às perguntas.");
    addMsg("log-respondedor",  "system", "SISTEMA", "O Respondedor também escolheu um animal em segredo!");
    atualizarTurno();
    await buscarPerguntaInvestigador();
  } catch(e) {
    addMsg("log-investigador", "fail", "ERRO", "Não foi possível conectar ao servidor.");
  }
}

// ── Atualiza visual do turno ──────────────────────────────
function atualizarTurno(){
  const banner     = document.getElementById("turno-texto");
  const invStatus  = document.getElementById("inv-status");
  const respStatus = document.getElementById("resp-status");
  const btns       = document.getElementById("resposta-btns");
  const respInput  = document.getElementById("resp-input");
  const respSend   = document.getElementById("btn-resp-send");

  if(turnoAtual === "investigador"){
    banner.textContent     = "TURNO: INVESTIGADOR";
    invStatus.textContent  = "ATIVO";
    invStatus.className    = "panel-status";
    respStatus.textContent = "AGUARDA";
    respStatus.className   = "panel-status aguarda";
    btns.querySelectorAll(".btn-resposta").forEach(b => b.disabled = false);
    respInput.disabled = true;
    respSend.disabled  = true;

  } else {
    banner.textContent     = "TURNO: RESPONDEDOR";
    invStatus.textContent  = "AGUARDA";
    invStatus.className    = "panel-status aguarda";
    respStatus.textContent = "ATIVO";
    respStatus.className   = "panel-status";
    btns.querySelectorAll(".btn-resposta").forEach(b => b.disabled = true);
    respInput.disabled = false;
    respSend.disabled  = false;
    respInput.focus();
  }
}

// ── Utilitário: adicionar mensagem ────────────────────────
function addMsg(logId, tipo, tag, texto){
  const log = document.getElementById(logId);
  const div = document.createElement("div");
  div.className = "msg msg-" + tipo;
  div.innerHTML = `<span class="msg-tag">${tag}</span>${texto}`;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

// ── Desabilita todos os controles (fim de jogo) ───────────
function desabilitarControles(){
  document.querySelectorAll(".btn-resposta").forEach(b => b.disabled = true);
  document.getElementById("resp-input").disabled = true;
  document.getElementById("btn-resp-send").disabled = true;
}

// =============================================================
//  INVESTIGADOR
// =============================================================

// Busca a próxima pergunta do Investigador no backend
async function buscarPerguntaInvestigador(){
  try {
    const res  = await fetch("/api/investigador/pergunta");
    const data = await res.json();

    if(data.encerrado){
      encerrarJogo(data.vencedor);
      return;
    }

    if(data.tipo === "chute"){
      // Investigador quer chutar — pede confirmação ao jogador
      aguardandoChute = "investigador";
      addMsg("log-investigador", "system", "INVESTIGADOR",
        `${data.mensagem} <br><small>Está correto? Use os botões abaixo.</small>`);
      mostrarBotoesChute("log-investigador", "investigador");
      return;
    }

    // Pergunta normal
    ultimaPerguntaInv = data.pergunta;
    addMsg("log-investigador", "system", "INVESTIGADOR",
      `${data.pergunta} <small style="color:var(--text-dim)">(${data.restantes} animais restantes)</small>`);

  } catch(e){
    addMsg("log-investigador", "fail", "ERRO", "Falha ao buscar pergunta do Investigador.");
  }
}

// Botões SIM / NÃO / NÃO SEI
document.getElementById("btn-sim").addEventListener("click",    () => responderInvestigador(true));
document.getElementById("btn-nao").addEventListener("click",    () => responderInvestigador(false));
document.getElementById("btn-naosei").addEventListener("click", () => responderInvestigador(null));

async function responderInvestigador(resposta){
  // Se estiver aguardando confirmação de chute, trata diferente
  if(aguardandoChute === "investigador"){
    await confirmarChuteInvestigador(resposta === true);
    return;
  }

  const labels = { true: "✔ SIM", false: "✘ NÃO", null: "? NÃO SEI" };
  addMsg("log-investigador", "user", "VOCÊ", labels[String(resposta)]);

  // Desabilita botões enquanto processa
  document.querySelectorAll(".btn-resposta").forEach(b => b.disabled = true);

  try {
    const res = await fetch("/api/investigador/resposta", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resposta }),
    });
    const data = await res.json();

    if(data.encerrado){ encerrarJogo(data.vencedor); return; }

    // Passa para o turno do Respondedor
    turnoAtual = "respondedor";
    atualizarTurno();
    await buscarPerguntaRespondedor();

  } catch(e){
    addMsg("log-investigador", "fail", "ERRO", "Falha ao enviar resposta.");
    document.querySelectorAll(".btn-resposta").forEach(b => b.disabled = false);
  }
}

async function confirmarChuteInvestigador(correto){
  aguardandoChute = null;
  removerBotoesChute("log-investigador");

  try {
    const res  = await fetch("/api/investigador/confirmar_chute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correto }),
    });
    const data = await res.json();

    if(data.vencedor){
      encerrarJogo("investigador");
    } else {
      addMsg("log-investigador", "fail", "SISTEMA", "Chute errado! Continuando...");
      turnoAtual = "respondedor";
      atualizarTurno();
      await buscarPerguntaRespondedor();
    }
  } catch(e){
    addMsg("log-investigador", "fail", "ERRO", "Falha ao confirmar chute.");
  }
}

// =============================================================
//  RESPONDEDOR
// =============================================================

async function buscarPerguntaRespondedor(){
  addMsg("log-respondedor", "system", "RESPONDEDOR", "Analisando...");

  try {
    const res  = await fetch("/api/respondedor/pergunta");
    const data = await res.json();

    // Remove a mensagem "Analisando..."
    const log = document.getElementById("log-respondedor");
    log.removeChild(log.lastChild);

    if(data.encerrado){ encerrarJogo(data.vencedor); return; }

    if(data.tipo === "chute"){
      aguardandoChute = "respondedor";
      addMsg("log-respondedor", "system", "RESPONDEDOR",
        `Eu sei qual é! É... ${data.animal}! <br><small>Está correto?</small>`);
      mostrarBotoesChute("log-respondedor", "respondedor");
      return;
    }

    // Pergunta normal
    ultimaPerguntaResp = data.pergunta;
    addMsg("log-respondedor", "system", "RESPONDEDOR", data.pergunta);

  } catch(e){
    addMsg("log-respondedor", "fail", "ERRO", "Falha ao buscar pergunta do Respondedor.");
  }
}

// Enviar resposta ao Respondedor
async function enviarRespostaRespondedor(){
  const input = document.getElementById("resp-input");
  const valor = input.value.trim();
  if(!valor) return;

  addMsg("log-respondedor", "user", "VOCÊ", valor);
  input.value = "";
  input.disabled = true;
  document.getElementById("btn-resp-send").disabled = true;

  try {
    await fetch("/api/respondedor/resposta", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: ultimaPerguntaResp, resposta: valor }),
    });

    // Passa para o turno do Investigador
    turnoAtual = "investigador";
    atualizarTurno();
    await buscarPerguntaInvestigador();

  } catch(e){
    addMsg("log-respondedor", "fail", "ERRO", "Falha ao enviar resposta.");
  }
}

document.getElementById("btn-resp-send").addEventListener("click", enviarRespostaRespondedor);
document.getElementById("resp-input").addEventListener("keydown", e => {
  if(e.key === "Enter") enviarRespostaRespondedor();
});

async function confirmarChuteRespondedor(correto){
  aguardandoChute = null;
  removerBotoesChute("log-respondedor");

  try {
    const res  = await fetch("/api/respondedor/confirmar_chute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correto }),
    });
    const data = await res.json();

    if(data.vencedor){
      encerrarJogo("respondedor");
    } else {
      addMsg("log-respondedor", "fail", "SISTEMA", "Chute errado! Continuando...");
      turnoAtual = "investigador";
      atualizarTurno();
      await buscarPerguntaInvestigador();
    }
  } catch(e){
    addMsg("log-respondedor", "fail", "ERRO", "Falha ao confirmar chute.");
  }
}

// =============================================================
//  CHUTES — botões de confirmação dinâmicos (SIM / NÃO)
// =============================================================

function mostrarBotoesChute(logId, agente){
  const log = document.getElementById(logId);
  const div = document.createElement("div");
  div.className   = "msg msg-system chute-confirmacao";
  div.id          = "chute-btns-" + agente;
  div.innerHTML   = `
    <span class="msg-tag">CONFIRME</span>
    <div style="display:flex;gap:8px;margin-top:6px">
      <button class="btn-resposta btn-sim"  onclick="confirmarChute('${agente}', true)">✔ SIM, ACERTOU</button>
      <button class="btn-resposta btn-nao"  onclick="confirmarChute('${agente}', false)">✘ NÃO, ERROU</button>
    </div>`;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;

  // Desabilita os botões principais enquanto aguarda confirmação
  if(agente === "investigador"){
    document.querySelectorAll(".btn-resposta:not(.chute-confirmacao .btn-resposta)")
      .forEach(b => b.disabled = true);
  }
}

function removerBotoesChute(logId){
  const el = document.getElementById(logId).querySelector(".chute-confirmacao");
  if(el) el.remove();
}

// Roteador de confirmação de chute
function confirmarChute(agente, correto){
  if(agente === "investigador") confirmarChuteInvestigador(correto);
  else                          confirmarChuteRespondedor(correto);
}

// =============================================================
//  FIM DE JOGO
// =============================================================

function encerrarJogo(vencedor){
  desabilitarControles();

  const msgs = {
    "investigador": {
      log:  "log-investigador",
      tipo: "success",
      txt:  "🏆 CASO ENCERRADO! Descobri seu animal!",
    },
    "respondedor": {
      log:  "log-respondedor",
      tipo: "success",
      txt:  "🏆 RESPONDEDOR VENCEU! Você adivinhou o animal!",
    },
  };

  const config = msgs[vencedor];
  if(config){
    addMsg(config.log, config.tipo, "FIM DE JOGO", config.txt);
    // Avisa o outro painel também
    const outroLog = config.log === "log-investigador" ? "log-respondedor" : "log-investigador";
    addMsg(outroLog, "fail", "FIM DE JOGO", "O adversário me venceu desta vez...");
  }

  document.getElementById("turno-texto").textContent = "JOGO ENCERRADO";
}