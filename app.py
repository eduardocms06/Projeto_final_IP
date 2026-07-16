from flask import Flask, jsonify, render_template, request
from src.jogo.partida import Partida
from src.llm.interpretador import interpretar_resposta


app = Flask(__name__, 
            template_folder='src/templates', 
            static_folder='src/templates/static')

partida = Partida()

@app.route("/")
def inicio():

    return render_template("index.html")

@app.post("/iniciar")
def iniciar():

    partida.iniciar()

    return jsonify({

        "status": "ok",

        "mensagem": "Partida iniciada."

    })

@app.get("/api/investigador/pergunta")
def pergunta_investigador():
    return jsonify(
        partida.obter_pergunta_investigador()
    )

@app.get("/animais")
def listar_animais():

    return jsonify(

        partida.listar_animais()

    )

@app.post("/escolher-animal")
def escolher_animal():

    dados = request.get_json()

    return jsonify(

        partida.escolher_animal(

            dados["animal"]

        )

    )

@app.post("/api/investigador/resposta")
def responder_investigador():

    dados = request.get_json()

    return jsonify(

        partida.responder_investigador(

            dados["caracteristica"],

            dados["mensagem"]

        )

    )

@app.get("/api/respondedor/pergunta")
def pergunta_respondedor():

    return jsonify(

        partida.obter_pergunta_respondedor()

    )

@app.post("/api/respondedor/resposta")
def responder_pergunta():

    dados = request.get_json()

    return jsonify(

        partida.responder_pergunta_jogador(

            dados["mensagem"]

        )

    )

@app.post("/api/investigador/confirmar_chute")
def confirmar_chute_investigador():

    dados = request.get_json()

    return jsonify(

        partida.confirmar_chute_investigador(

            dados["correto"]

        )

    )


if __name__ == "__main__":

    app.run(
        debug=True
    )