import requests

OLLAMA_URL = "http://localhost:11434"

EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.1"


def gerar_embedding(texto: str):

    resposta = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": texto
        }
    )

    resposta.raise_for_status()

    return resposta.json()["embeddings"][0]


def gerar_resposta(prompt: str):

    resposta = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    resposta.raise_for_status()

    return resposta.json()["response"]