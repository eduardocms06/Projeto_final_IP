import os
import json


def carregar_animais():

    animais = []

    pasta_animais = "dados/animais"

    for arquivo in os.listdir(pasta_animais):

        if arquivo.endswith(".json"):

            caminho = os.path.join(
                pasta_animais,
                arquivo
            )

            with open(
                caminho,
                "r",
                encoding="utf-8"
            ) as f:

                animal = json.load(f)

                animais.append(animal)

    return animais


def carregar_caracteristicas():

    with open(
        "dados/caracteristicas/caracteristicasAnimais.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)