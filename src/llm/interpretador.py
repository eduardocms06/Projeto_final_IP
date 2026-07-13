import requests


def interpretar_resposta(pergunta, resposta_usuario):

    prompt = f"""
Você é um interpretador.

Sua única tarefa é analisar a resposta do usuário.

Pergunta:
{pergunta}

Resposta do usuário:
{resposta_usuario}

Responda SOMENTE com:

TRUE

ou

FALSE

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

    texto = resposta.json()["response"]

    print("================================")
    print(texto)
    print("================================")

    texto = texto.strip().upper()

    return texto == "TRUE"