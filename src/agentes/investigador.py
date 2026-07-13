def filtrar_animais(
    animais,
    caracteristica,
    resposta
):

    animais_restantes = []

    for animal in animais:

        if animal.get(caracteristica, False) == resposta:

            animais_restantes.append(animal)

    return animais_restantes

def contar_respostas(animais, caracteristica):

    sim = 0
    nao = 0

    for animal in animais:

        if animal.get(caracteristica, False):

            sim += 1

        else:

            nao += 1

    return sim, nao


def melhor_pergunta(
    animais,
    caracteristicas,
    perguntas_feitas
):

    melhor_caracteristica = None

    melhor_diferenca = float("inf")

    for caracteristica in caracteristicas.keys():

        if caracteristica in perguntas_feitas:

            continue

        sim, nao = contar_respostas(
            animais,
            caracteristica
        )

        if sim == 0 or nao == 0:

            continue

        diferenca = abs(
            sim - nao
        )

        if diferenca < melhor_diferenca:

            melhor_diferenca = diferenca

            melhor_caracteristica = caracteristica

    return melhor_caracteristica