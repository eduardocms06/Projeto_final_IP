from flask import Flask, jsonify, render_template, request
from src.jogo.partida import Partida
from src.llm.interpretador import interpretar_resposta


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

@app.post("/responder-ia")
def responder_ia():

    dados = request.get_json()

    partida.ia.atualizar_animais(

        dados["caracteristica"],

        dados["resposta"]

    )

    pergunta = partida.ia.escolher_pergunta()

    return jsonify({

        "caracteristica": pergunta,

        "pergunta": partida.caracteristicas[pergunta],

        "restantes": partida.ia.quantidade_restante()

    })

@app.post("/mensagem")
def mensagem():

    dados = request.get_json()

    mensagem = dados["mensagem"]

    caracteristica = dados["caracteristica"]

    pergunta = partida.caracteristicas[caracteristica]

    resposta = interpretar_resposta(
        pergunta,
        mensagem
    )

    partida.ia.atualizar_animais(
        caracteristica,
        resposta
    )

    proxima = partida.ia.escolher_pergunta()

    return jsonify({

        "caracteristica": proxima,

        "pergunta": partida.caracteristicas[proxima],

        "restantes": partida.ia.quantidade_restante()

    })


if __name__ == "__main__":

    app.run(
        debug=True
    )