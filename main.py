from utils.carregador import (
    carregar_animais,
    carregar_caracteristicas
)

from agentes.investigador import (
    melhor_pergunta,
    filtrar_animais
)


animais = carregar_animais()

caracteristicas = carregar_caracteristicas()

perguntas_feitas = []

print("\nPense em um animal...\n")

while len(animais) > 1:

    print("\n==============================")
    print(f"Animais restantes: {len(animais)}")
    print("==============================")
    
    if len(animais) <= 10:
        print("\nAnimais possíveis:")
        for animal in animais:
           print("-", animal["nome"])

    pergunta = melhor_pergunta(
        animais,
        caracteristicas,
        perguntas_feitas
    )

    if pergunta is None:
        break

    perguntas_feitas.append(pergunta)

    print("\n" + caracteristicas[pergunta])

    resposta_usuario = input("(s/n): ").lower()

    resposta = resposta_usuario == "s"

    animais = filtrar_animais(
        animais,
        pergunta,
        resposta
    )

if len(animais) == 1:

    print("\n==============================")
    print("ANIMAL ENCONTRADO")
    print("==============================")

    print(
        f"\nEu acho que seu animal é: {animais[0]['nome']}"
    )

elif len(animais) > 1:

    print("\nNão consegui diferenciar os seguintes animais:")

    for animal in animais:
        print("-", animal["nome"])

else:

    print("\nNenhum animal corresponde às respostas.")