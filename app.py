from flask import Flask, jsonify, render_template, request
from src.jogo.partida import Partida


app = Flask(__name__)

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

@app.get("/animais")
def listar_animais():

    animais = []

    for animal in partida.animais:

        animais.append(
            animal["nome"]
        )

    return jsonify(animais)

@app.post("/escolher-animal")
def escolher_animal():

    dados = request.get_json()

    nome = dados["animal"]

    for animal in partida.animais:

        if animal["nome"] == nome:

            partida.jogador.escolher_animal(
                animal
            )

            break

    return jsonify({

        "status": "ok"

    })

@app.get("/pergunta-ia")
def pergunta_ia():

    pergunta = partida.ia.escolher_pergunta()

    return jsonify({

        "caracteristica": pergunta,

        "pergunta": partida.caracteristicas[pergunta]

    })


if __name__ == "__main__":

    app.run(
        debug=True
    )