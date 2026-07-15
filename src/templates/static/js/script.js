
// ── Navegação entre telas - alternando qual das .screen está visivel naquele momento.
function showScreen(id){
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));    // Seleciona as três telas, e remove a classe active de cada um, escondendo-as
  
  //Monta o ID e adiciona a classe active para a tela desejada.
  document.getElementById("screen-" + id).classList.add("active");
}
//Ao clicar no botão modalidades, leva para a tela de "modalidades"
document.getElementById("btn-modalidades").addEventListener("click", () => showScreen("modalidades"));

// Faz com que qualquer elemento que tenha o atributo "data-destino" navegue para a tela especificada no valor do atributo
document.querySelectorAll("[data-destino]").forEach(btn => {
  btn.addEventListener("click", () => showScreen(btn.getAttribute("data-destino")));
});

// Bloco voltado para o botão SAIR
// Armazena a referência do overlay de encerramento
const shutdownOverlay = document.getElementById("shutdown-overlay");

// Exibe a tela preta de "Encerrando sessão" ao clicar em SAIR
document.getElementById("btn-sair").addEventListener("click", () => shutdownOverlay.classList.add("active"));

// ao clicar em RECONECTAR esconde a tela de encerramento e devolve o jogador ao jogo
document.getElementById("btn-reconectar").addEventListener("click", () => shutdownOverlay.classList.remove("active"));

// `Parte da seleção das modalidades`
// Adiciona um listener de clique a todos os cards de modalidade disponíveis
document.querySelectorAll(".mod-card").forEach(card => {

// Ao clicar no card, identifica a modalidade escolhida e inicia o chat correspondente
  card.addEventListener("click", () => abrirChat(card.getAttribute("data-modalidade")));
});

// Estado local do front end
let turnoAtual        = "investigador";       // indica de quem é o turno ativo
let ultimaPerguntaInv = "";                   // Armazena o texto da pergunta atual do Investigador
let ultimaPerguntaResp= "";                   // Armazena o texto da pergunta atual do Respondedor
let aguardandoChute   = null;                 // "investigador" | "respondedor" | null

// Inicializa a tela de chat de uma partida
async function abrirChat(modalidadeId){
  //Configura a ID visual do cabeçalho do chat
  document.getElementById("chat-title").textContent = modalidadeId === "1" ? "ANIMAIS" : "FRUTAS";
  document.getElementById("chat-ref").textContent   = "REF: MOD-0" + modalidadeId;

  //Limpa o histórico de partidas anteriores
  document.getElementById("log-investigador").innerHTML = "";
  document.getElementById("log-respondedor").innerHTML  = "";

  //Reinicia o estado lógico global
  turnoAtual         = "investigador";
  ultimaPerguntaInv  = "";
  ultimaPerguntaResp = "";
  aguardandoChute    = null;

  //Transiciona a interface para a tela de chat
  showScreen("chat");

  // Inicia partida no backend
  try {
    // Faz a requisição POST assíncrona para registrar o início no backend
    const res = await fetch("/api/jogo/iniciar", { method: "POST" });
    const data = await res.json();

    //Insere as orientações iniciais nos logs do jogo
    addMsg("log-investigador", "system", "SISTEMA", "Pense em um animal e responda às perguntas.");
    addMsg("log-respondedor",  "system", "SISTEMA", "O Respondedor também escolheu um animal em segredo!");
    // Prepara os painéis da interface conforme o turno do Investigador
    atualizarTurno();
    // Executa a busca assíncrona da pergunta inicial do Investigador
    await buscarPerguntaInvestigador();

    //Caso ocorrer erro, exibe uma mensagem.
  } catch(e) {
    addMsg("log-investigador", "fail", "ERRO", "Não foi possível conectar ao servidor.");
  }
}

// CONTROLE VISUAL
 /**
 * Atualiza a interface gráfica do chat com base no turnoAtual.
 * Habilita os botões de quem deve jogar e desabilita os outros botões e ajusta
 * os textos e classes de "Ativo" / "Aguarda" nos painéis.
 */
function atualizarTurno(){
  const banner     = document.getElementById("turno-texto");
  const invStatus  = document.getElementById("inv-status");
  const respStatus = document.getElementById("resp-status");
  const btns       = document.getElementById("resposta-btns");
  const respInput  = document.getElementById("resp-input");
  const respSend   = document.getElementById("btn-resp-send");
  // 2. Aplica o estado visual do turno do INVESTIGADOR
  if(turnoAtual === "investigador"){
    banner.textContent     = "TURNO: INVESTIGADOR";

    // Ativa o painel do Investigador
    invStatus.textContent  = "ATIVO";
    invStatus.className    = "panel-status";

    // Coloca o painel do Respondendor em aguardo
    respStatus.textContent = "AGUARDA";
    respStatus.className   = "panel-status aguarda";

    // Libera o clique nos botões de opções do investigador S/N/NS
    btns.querySelectorAll(".btn-resposta").forEach(b => b.disabled = false);

    //Bloqueia a barra de digitação do respondedor
    respInput.disabled = true;
    respSend.disabled  = true;
    //Controla o estado visual do RESPONDEDOR
  } else {
    banner.textContent     = "TURNO: RESPONDEDOR";

    // Ativa o painel do RESPONDEDOR
    invStatus.textContent  = "AGUARDA";
    invStatus.className    = "panel-status aguarda";

    // Coloca o painel do Investigador em aguardo
    respStatus.textContent = "ATIVO";
    respStatus.className   = "panel-status";

    //desabilita os botões do respondedor
    btns.querySelectorAll(".btn-resposta").forEach(b => b.disabled = true);

    //Libera a barra de digitação do respondedor
    respInput.disabled = false;
    respSend.disabled  = false;
    respInput.focus();
  }
}

// Cria dinamicamente um balão de mensagem e o injeta na tela de chat.
function addMsg(logId, tipo, tag, texto){
  const log = document.getElementById(logId);

  // Cria a div que representa o contêiner da mensagem
  const div = document.createElement("div");

  // Concatena a classe base com a do tipo para receber o CSS correspondente
  div.className = "msg msg-" + tipo;

  // Insere a tag de nome e o texto no formato HTML
  div.innerHTML = `<span class="msg-tag">${tag}</span>${texto}`;

  //A nova mensagem é anexada no final do histórico
  log.appendChild(div);

  log.scrollTop = log.scrollHeight;
}

// Desabilita todos os controles ao chegar no fim de jogo 
function desabilitarControles(){
  //btn investigador
  document.querySelectorAll(".btn-resposta").forEach(b => b.disabled = true);
  //btn de envio e input do respondedor
  document.getElementById("resp-input").disabled = true;
  document.getElementById("btn-resp-send").disabled = true;
}

// Consulta o backend para obter a próxima pergunta do Investigador.
async function buscarPerguntaInvestigador(){
  try {
    // Busca os dados da próxima jogada via requisição GET
    const res  = await fetch("/api/investigador/pergunta");
    const data = await res.json();

    // Verifica se o servidor determinou o fim da partida
    if(data.encerrado){
      encerrarJogo(data.vencedor);
      return;
    }
    //Verifica se a IA tem a certeza para poder arriscar o chute
    if(data.tipo === "chute"){

      // Investigador quer chutar — pede confirmação ao jogador
      aguardandoChute = "investigador";

      // Exibe o palpite formatado com um texto de instrução extra
      addMsg("log-investigador", "system", "INVESTIGADOR",
        `${data.mensagem} <br><small>Está correto? Use os botões abaixo.</small>`);

      // botões auxiliares para o jogador confirmar ou negar o chute
      mostrarBotoesChute("log-investigador", "investigador");
      return;
    }

    // Pergunta normal salvando-a no estado global
    ultimaPerguntaInv = data.pergunta;

    //exibe a pergunta acompanhada da contagem de animais que restam na lógica da IA
    addMsg("log-investigador", "system", "INVESTIGADOR",
      `${data.pergunta} <small style="color:var(--text-dim)">(${data.restantes} animais restantes)</small>`);

    //exibe balão de mensagem em caso de erro.
  } catch(e){
    addMsg("log-investigador", "fail", "ERRO", "Falha ao buscar pergunta do Investigador.");
  }
}

//Associa os botões como chamadas de envio de resposta
document.getElementById("btn-sim").addEventListener("click",    () => responderInvestigador(true));
document.getElementById("btn-nao").addEventListener("click",    () => responderInvestigador(false));
document.getElementById("btn-naosei").addEventListener("click", () => responderInvestigador(null));

//Processa a resposta dada pelo usuário à pergunta do Investigador. enviando para o BackEnd e transitando o turno
async function responderInvestigador(resposta){
  // Se estiver aguardando confirmação de chute, trata diferente
  if(aguardandoChute === "investigador"){
    //Se o jogador confirmar que o chute está correto, Interrompe a função.
    await confirmarChuteInvestigador(resposta === true);
    return;
  }
  //Manipulação dos rótulos visuais para a cofnirmação.
  const labels = { true: "✔ SIM", false: "✘ NÃO", null: "? NÃO SEI" };
  //converte o valor para strings
  addMsg("log-investigador", "user", "VOCÊ", labels[String(resposta)]);

  // Desabilita botões enquanto processa
  document.querySelectorAll(".btn-resposta").forEach(b => b.disabled = true);
  //envia a resposta para o investigador analisar
  try {
    const res = await fetch("/api/investigador/resposta", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resposta }),     //envia em formato de dicionario.
    });
    const data = await res.json();

    if(data.encerrado){ encerrarJogo(data.vencedor); return; }          // Se o jogo acabou com essa resposta, executa a rotina de fim de jogo
  
    // Passa para o turno do Respondedor
    turnoAtual = "respondedor";
    atualizarTurno();       // Atualiza os controles visuais na tela
    await buscarPerguntaRespondedor();      // Busca a pergunta que o jogador deve responder
    // Em caso de erro, avisa o usuário e reabilita os botões para nova tentativa
  } catch(e){
    addMsg("log-investigador", "fail", "ERRO", "Falha ao enviar resposta.");
    document.querySelectorAll(".btn-resposta").forEach(b => b.disabled = false);
  }
}
// Avisa ao backend se o palpite final do Investigador estava certo ou errado.
async function confirmarChuteInvestigador(correto){
  aguardandoChute = null;
  removerBotoesChute("log-investigador");

  try {
    //Envia a confirmação para a rota do Investigador no servidor
    const res  = await fetch("/api/investigador/confirmar_chute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correto }),
    });
    const data = await res.json();
    
    //Se a IA acertou, o servidor sinaliza a vitória
    if(data.vencedor){
      encerrarJogo("investigador");

      //Se a IA errou o chute, o jogo prossegue
    } else {
      addMsg("log-investigador", "fail", "SISTEMA", "Chute errado! Continuando...");

      // Inicia a transição de turno passando a vez para o Respondedor
      turnoAtual = "respondedor";
      atualizarTurno();
      await buscarPerguntaRespondedor();
    }
  } catch(e){
    addMsg("log-investigador", "fail", "ERRO", "Falha ao confirmar chute.");
  }
}
// Consulta o backend para obter a próxima pergunta do Respondedor.
async function buscarPerguntaRespondedor(){
  // Exibe uma mensagem temporária para demonstrar que o jogo não travou
  addMsg("log-respondedor", "system", "RESPONDEDOR", "Analisando...");

  try {
    // Busca os dados da jogada
    const res  = await fetch("/api/respondedor/pergunta");
    const data = await res.json();

    // Remove a mensagem "Analisando..."
    const log = document.getElementById("log-respondedor");
    log.removeChild(log.lastChild);

    //Indica fim do jogo
    if(data.encerrado){ encerrarJogo(data.vencedor); return; }
    
    // Verifica se a IA tem certeza do seu palpite final
    if(data.tipo === "chute"){
      aguardandoChute = "respondedor";

      //Monta a mensagem visual com a variável do animal que a IA pensou
      addMsg("log-respondedor", "system", "RESPONDEDOR",
        `Eu sei qual é! É... ${data.animal}! <br><small>Está correto?</small>`);
        // Renderiza os botões de Sim/Não no painel do Respondedor
      mostrarBotoesChute("log-respondedor", "respondedor");
      return;
    }

    // Pergunta normal salva o texto
    ultimaPerguntaResp = data.pergunta;
    addMsg("log-respondedor", "system", "RESPONDEDOR", data.pergunta);
    //exibe mensagem de erro
  } catch(e){
    addMsg("log-respondedor", "fail", "ERRO", "Falha ao buscar pergunta do Respondedor.");
  }
}

// Processa o texto digitado pelo jogador ao responder uma pergunta da IA e envia ao Back-End
async function enviarRespostaRespondedor(){
  // Obtém as referências do formulário
  const input = document.getElementById("resp-input");
  //Limpa espaços acidentais do inicio e fim
  const valor = input.value.trim();
  //Se o usuário clicar sem digitar nada, o envio é abortado
  if(!valor) return;

  addMsg("log-respondedor", "user", "VOCÊ", valor);
  //Limpa o texto da caixa de digitação e desabilita os controles
  input.value = "";
  input.disabled = true;
  document.getElementById("btn-resp-send").disabled = true;

  try {
    //Envia a resposta ao backend de forma assíncrona
    await fetch("/api/respondedor/resposta", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: ultimaPerguntaResp, resposta: valor }),    //reenvia o contexto salvo no estado global
    });

    // Tranferência de Turno para o Investigador
    turnoAtual = "investigador";
    atualizarTurno();
    await buscarPerguntaInvestigador();    

  } catch(e){
    addMsg("log-respondedor", "fail", "ERRO", "Falha ao enviar resposta.");
  }
}
//Controles do respondedor

// Dispara o envio quando o usuário clica no botão com o mouse/dedo
document.getElementById("btn-resp-send").addEventListener("click", enviarRespostaRespondedor);

// Monitora o teclado enquanto o usuário digita no input
document.getElementById("resp-input").addEventListener("keydown", e => {
  //Atalho pra enviar com a tecla enter
  if(e.key === "Enter") enviarRespostaRespondedor();
});

//Processa a resposta do usuário quanto a IA tenta adivinhar o animal.
async function confirmarChuteRespondedor(correto){
  //Limpa sinalizando que não tem nenhum chute e botões de confirmação pendente.
  aguardandoChute = null;
  removerBotoesChute("log-respondedor");

  try {
    //Envia o veredito para a rota correspondente no backend
    const res  = await fetch("/api/respondedor/confirmar_chute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correto }),
    });
    const data = await res.json();

    //Se a IA acertou o animal, o servidor decreta o fim de jogo
    if(data.vencedor){
      encerrarJogo("respondedor");

      // Se a IA errou, a partida continua e o turno muda
    } else {
      addMsg("log-respondedor", "fail", "SISTEMA", "Chute errado! Continuando...");
      // Devolve a vez de jogar para o agente Investigador
      turnoAtual = "investigador";
      atualizarTurno();
      await buscarPerguntaInvestigador();  // Busca a próxima pergunta do Investigador
    }
  } catch(e){
    addMsg("log-respondedor", "fail", "ERRO", "Falha ao confirmar chute.");
  }
}

//Cria botões especiais de "sim, acertou e "não, errou"
function mostrarBotoesChute(logId, agente){
  const log = document.getElementById(logId);
  const div = document.createElement("div");

  // Atribui uma classe específica para poder identificar e remover essa div depois
  div.className   = "msg msg-system chute-confirmacao";
  div.id          = "chute-btns-" + agente;
  //HTML interno com botões, que disparam a função global de 'confirmarChute'
  div.innerHTML   = `
    <span class="msg-tag">CONFIRME</span>
    <div style="display:flex;gap:8px;margin-top:6px">
      <button class="btn-resposta btn-sim"  onclick="confirmarChute('${agente}', true)">✔ SIM, ACERTOU</button>
      <button class="btn-resposta btn-nao"  onclick="confirmarChute('${agente}', false)">✘ NÃO, ERROU</button>
    </div>`;
  log.appendChild(div);
  //Mantém a rolagem no fim da tela
  log.scrollTop = log.scrollHeight;

  // Desabilita os botões principais enquanto aguarda confirmação
  if(agente === "investigador"){

    // Seleciona todos os botões de resposta, EXCETO o que foi criado internamente
    document.querySelectorAll(".btn-resposta:not(.chute-confirmacao .btn-resposta)")
      .forEach(b => b.disabled = true);
  }
}
//Procura e destrói os botões temporários
function removerBotoesChute(logId){
  // Busca especificamente o elemento com a classe indicadora dentro do log fornecido
  const el = document.getElementById(logId).querySelector(".chute-confirmacao");
  if(el) el.remove();
}

// Roteador de confirmação de chute
function confirmarChute(agente, correto){
  if(agente === "investigador") confirmarChuteInvestigador(correto);
  else                          confirmarChuteRespondedor(correto);
}


//  FIM DE JOGO
//Gerencia os procedimentos visuais e interativos do fim de jogo.
function encerrarJogo(vencedor){

  desabilitarControles();
  // Cria um dicionário (objeto aninhado) com as configurações visuais de vitória
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
  //Acessa dinamicamente os dados do vencedor
  const config = msgs[vencedor];
  //Identifica se é vencedor e processa as mensagens de fim de jogo.
  if(config){
    //Exibe mensagem de vitória no chat de quem venceu.
    addMsg(config.log, config.tipo, "FIM DE JOGO", config.txt);
    // Avisa o outro painel também
    const outroLog = config.log === "log-investigador" ? "log-respondedor" : "log-investigador";
    //exibe balão de fracasso na tela de quem perdeu.
    addMsg(outroLog, "fail", "FIM DE JOGO", "O adversário me venceu desta vez...");
  }
  //Altera o Banner superior para sinalizar o fim do jogo.
  document.getElementById("turno-texto").textContent = "JOGO ENCERRADO";
}