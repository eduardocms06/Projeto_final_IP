import requests


def interpretar_pergunta(pergunta_usuario, perguntas):

    lista = ""

    for chave, pergunta in perguntas.items():

        lista += f"{chave} -> {pergunta}\n"

    prompt = f"""
Você é um interpretador de perguntas.

Sua função é descobrir qual característica o usuário está perguntando.

Características disponíveis:

{lista}

Pergunta do usuário:

{pergunta_usuario}

Responda SOMENTE com o nome da característica.

Exemplos:

Pergunta:
"O animal voa?"

Resposta:
voa

Pergunta:
"Ele vive no oceano?"

Resposta:
vive_oceano

Não explique.
"""

    resposta = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model": "llama3",

            "prompt": prompt,

            "stream": False

        }

    )

    return resposta.json()["response"].strip()