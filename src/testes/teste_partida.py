from src.jogo.partida import Partida


partida = Partida()

partida.iniciar()

print("=" * 50)
print("JOGO INICIADO")
print("=" * 50)

print()

print("Animal escolhido pela IA:")

print(partida.ia.animal_escolhido["nome"])

print()

print("Quantidade de animais:")

print(len(partida.animais))