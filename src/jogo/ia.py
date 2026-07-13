import random

from src.agentes.investigador import (
    melhor_pergunta,
    filtrar_animais
)


class IA:

    def __init__(self, animais, caracteristicas):

        # Lista completa de animais
        self.animais = animais

        # Lista de candidatos restantes para descobrir o animal do jogador
        self.animais_possiveis = animais.copy()

        # Características disponíveis
        self.caracteristicas = caracteristicas

        # Perguntas já realizadas
        self.perguntas_feitas = []

        # Histórico da partida
        self.historico = []

        # Animal secreto da IA
        self.animal_escolhido = None

    def escolher_animal(self):
        """
        Escolhe aleatoriamente o animal da IA.
        """

        self.animal_escolhido = random.choice(self.animais)

    def responder(self, caracteristica):
        """
        Responde True ou False para uma característica perguntada pelo jogador.
        """

        return self.animal_escolhido.get(
            caracteristica,
            False
        )

    def escolher_pergunta(self):

        pergunta = melhor_pergunta(
            self.animais_possiveis,
            self.caracteristicas,
            self.perguntas_feitas
        )

        if pergunta:

            self.perguntas_feitas.append(pergunta)

        return pergunta
    
    def mostrar_debug(self):

        print("\n========== DEBUG ==========")

        print(f"Animais restantes: {len(self.animais_possiveis)}")

        print()

        for animal in self.animais_possiveis:

            print("-", animal["nome"])

        print()

        print("Perguntas feitas:")

        print(self.perguntas_feitas)

        print("===========================\n")

    def atualizar_animais(self, caracteristica, resposta):
        """
        Atualiza a lista de animais possíveis após receber uma resposta.
        """

        self.historico.append({

            "caracteristica": caracteristica,

            "resposta": resposta

        })

        self.animais_possiveis = filtrar_animais(
            self.animais_possiveis,
            caracteristica,
            resposta
        )

    def quantidade_restante(self):
        """
        Retorna quantos animais ainda são possíveis.
        """

        return len(self.animais_possiveis)

    def pode_adivinhar(self):
        """
        Verifica se já restou apenas um animal.
        """

        return len(self.animais_possiveis) == 1

    def palpite(self):
        """
        Retorna o animal restante caso exista apenas um.
        """

        if self.pode_adivinhar():

            return self.animais_possiveis[0]

        return None

    def verificar_palpite(self, animal):
        """
        Verifica se o jogador acertou o animal escolhido pela IA.
        """

        return (
            animal.lower().strip()
            ==
            self.animal_escolhido["nome"].lower().strip()
        )

    def obter_historico(self):
        """
        Retorna o histórico das perguntas feitas pela IA.
        """

        return self.historico

    def reiniciar(self):
        """
        Reinicia o estado da IA para uma nova partida.
        """

        self.animais_possiveis = self.animais.copy()

        self.perguntas_feitas = []

        self.historico = []

        self.animal_escolhido = None