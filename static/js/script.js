/* =========================================================
   QUEM SOU EU? — Front-end (navegação e interações visuais)
   Sem dados/lógica de jogo — a integração com o backend
   (dados das modalidades, pistas, verificação de palpite etc.)
   deverá ser implementada posteriormente.
   ========================================================= */

// ---------- Navegação entre telas ----------
function showScreen(id){
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById("screen-" + id).classList.add("active");
}

document.getElementById("btn-modalidades").addEventListener("click", () => {
  showScreen("modalidades");
});

document.querySelectorAll("[data-destino]").forEach(btn => {
  btn.addEventListener("click", () => {
    showScreen(btn.getAttribute("data-destino"));
  });
});

// ---------- Botão SAIR ----------
const shutdownOverlay = document.getElementById("shutdown-overlay");
document.getElementById("btn-sair").addEventListener("click", () => {
  shutdownOverlay.classList.add("active");
});
document.getElementById("btn-reconectar").addEventListener("click", () => {
  shutdownOverlay.classList.remove("active");
});

// ---------- Seleção de modalidade ----------
// Ao clicar em um card, abre a tela de chat.
// TODO (backend): usar o atributo data-modalidade para buscar
// os dados reais do dossiê (título, referência, pistas, identidade oculta etc.)
document.querySelectorAll(".mod-card").forEach(card => {

    card.addEventListener("click", async () => {

        const modalidadeId = card.getAttribute("data-modalidade");

        await iniciarPartida();

        await abrirChat(modalidadeId);

    });

});

async function iniciarPartida() {

    const resposta = await fetch("/iniciar", {

        method: "POST"

    });

    return await resposta.json();

}

async function obterAnimais() {

    const resposta = await fetch("/animais");

    return await resposta.json();

}

async function abrirChat(modalidadeId){
  // Placeholder de cabeçalho — substituir pelos dados reais da modalidade escolhida.
  document.getElementById("chat-title").textContent = "MODALIDADE " + modalidadeId;
  document.getElementById("chat-ref").textContent = "REF: MOD-0" + modalidadeId;

  // Reseta o log e os campos da tela de chat.
  document.getElementById("chat-log").innerHTML = "";
  const animais = await obterAnimais();

  mostrarListaAnimais(animais);
  document.getElementById("chat-input").value = "";
  document.getElementById("chat-input").disabled = false;
  document.getElementById("btn-send").disabled = false;


  showScreen("chat");
  document.getElementById("chat-input").focus();
}

// ---------- Utilitário para exibir mensagens no chat ----------
// tipo: "system" | "user" | "success" | "fail"
function addMsg(tipo, tag, texto){
  const log = document.getElementById("chat-log");
  const div = document.createElement("div");
  div.className = "msg msg-" + tipo;
  div.innerHTML = `<span class="msg-tag">${tag}</span>${texto}`;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function mostrarListaAnimais(animais) {

    addMsg(
        "system",
        "IA",
        "Escolha o seu animal:"
    );

    const log = document.getElementById("chat-log");

    const container = document.createElement("div");

    container.id = "lista-animais";

    const botoes = [];

    animais.forEach(animal => {

        const botao = document.createElement("button");

        botoes.push(botao);

        botao.textContent = animal;

        botao.className = "btn-animal";

        botao.addEventListener("click", async () => {

            container.remove();

            const resposta = await fetch("/escolher-animal", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    animal: animal

                })

            });

            const pergunta = await obterPerguntaIA();

            const dados = await resposta.json();

            console.log(dados)

            addMsg(
                "user",
                "VOCÊ",
                "Escolhi: " + animal
            );

            addMsg(
                "system",
                "IA",
                "Perfeito! Já escolhi meu animal também.<br>Vamos começar!"
            );

            addMsg(
                "system",
                "IA",
                "Perfeito! Já escolhi meu animal também.<br><br>" +
                pergunta.pergunta
            );

        });

        container.appendChild(botao);

    });

    log.appendChild(container);

    log.scrollTop = log.scrollHeight;

}

async function obterPerguntaIA() {

    const resposta = await fetch("/pergunta-ia");

    return await resposta.json();

}

// ---------- Enviar palpite / mensagem ----------
// TODO (backend): validar o palpite contra a identidade oculta,
// atualizar tentativas e encerrar o caso quando resolvido.
function enviarMensagem(){
  const input = document.getElementById("chat-input");
  const valor = input.value.trim();
  if (!valor) return;

  addMsg("user", "VOCÊ", valor);
  input.value = "";
}

document.getElementById("btn-send").addEventListener("click", enviarMensagem);
document.getElementById("chat-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") enviarMensagem();
});
