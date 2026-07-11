import json
import re
from pathlib import Path


OVERLAP = 100
CHUNK_SIZE = 800


def ler_arquivo(caminho: Path):

    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


# ------------------------
# PYTHON
# ------------------------

def chunk_python(texto):

    partes = re.split(r'(?=^class\s+|^def\s+)', texto, flags=re.MULTILINE)

    return [p.strip() for p in partes if p.strip()]


# ------------------------
# JSON
# ------------------------

def chunk_json(texto):
    try:
        dados = json.loads(texto)

        if not isinstance(dados, dict):
            return [json.dumps(dados, indent=2, ensure_ascii=False)]

        linhas = []

        nome = dados.get("nome", "Desconhecido")
        linhas.append(f"Animal: {nome}")
        linhas.append("")
        linhas.append("Características:")

        for chave, valor in dados.items():

            if chave == "nome":
                continue

            if valor is True:
                texto_chave = chave.replace("_", " ")
                linhas.append(f"- {texto_chave}")

            elif valor is False:
                continue

            else:
                texto_chave = chave.replace("_", " ")
                linhas.append(f"- {texto_chave}: {valor}")

        return ["\n".join(linhas)]

    except Exception:
        return [texto]

# ------------------------
# MARKDOWN
# ------------------------

def chunk_markdown(texto):

    partes = re.split(r'(?=^#)', texto, flags=re.MULTILINE)

    return [p.strip() for p in partes if p.strip()]


# ------------------------
# PADRÃO
# ------------------------

def chunk_generico(texto):

    chunks = []

    inicio = 0

    while inicio < len(texto):

        fim = inicio + CHUNK_SIZE

        chunks.append(texto[inicio:fim])

        inicio += CHUNK_SIZE - OVERLAP

    return chunks


# ------------------------
# PRINCIPAL
# ------------------------

def processar_arquivo(caminho: Path):

    texto = ler_arquivo(caminho)

    extensao = caminho.suffix.lower()

    if extensao == ".py":
        return chunk_python(texto)

    if extensao == ".json":
        return chunk_json(texto)

    if extensao == ".md":
        return chunk_markdown(texto)

    return chunk_generico(texto)