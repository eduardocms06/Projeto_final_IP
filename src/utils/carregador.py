from pathlib import Path
import json

# Raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[2]

PASTA_ANIMAIS = BASE_DIR / "data" / "animais"

ARQUIVO_CARACTERISTICAS = (
    BASE_DIR
    / "data"
    / "caracteristicas"
    / "caracteristicasAnimais.json"
)


def carregar_animais():

    animais = []

    for arquivo in PASTA_ANIMAIS.glob("*.json"):

        with open(
            arquivo,
            encoding="utf-8"
        ) as f:

            animais.append(
                json.load(f)
            )

    return animais


def carregar_caracteristicas():

    with open(
        ARQUIVO_CARACTERISTICAS,
        encoding="utf-8"
    ) as f:

        return json.load(f)