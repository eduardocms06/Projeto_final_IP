from src.jogo.ia import IA
from src.jogo.jogador import Jogador
from src.agentes.respondedor import pergunta_para_texto
from src.llm.interpretador_pergunta import interpretar_pergunta

from src.utils.carregador import (
    carregar_animais,
    carregar_caracteristicas
)


class Partida:

    def __init__(self):

        self.animais = carregar_animais()

        self.caracteristicas = carregar_caracteristicas()

        self.ia = IA(
            self.animais,
            self.caracteristicas
        )

        # Cria o jogador
        self.jogador = Jogador()

        self.turno = 1

        self.jogo_finalizado = False

        self.estado = "ESCOLHENDO_ANIMAL"



    def mostrar_cabecalho(self):

        print()
        print("=" * 60)
        print("🐾            QUEM SOU EU?            🐾")
        print("=" * 60)


    def mostrar_inicio_rodada(self):

        print()
        print("=" * 60)
        print(f"🎲 RODADA {self.turno}")
        print("=" * 60)


    def mostrar_vez_jogador(self):

        print()
        print("🎮 VEZ DO JOGADOR")
        print("-" * 60)


    def mostrar_vez_ia(self):

        print()
        print("🤖 VEZ DA IA")
        print("-" * 60)


    def mostrar_resumo_ia(self):

        print()
        print("-" * 60)
        print(f"📊 Animais restantes para a IA: {self.ia.quantidade_restante()}")
        print("-" * 60)


    def mostrar_vencedor(self, vencedor):

        print()
        print("=" * 60)

        if vencedor == "jogador":
            print("🏆 PARABÉNS! VOCÊ VENCEU!")

        else:
            print("🤖 A IA VENCEU!")

        print("=" * 60)

    def iniciar(self):

        self.ia.reiniciar()

        self.ia.escolher_animal()

        self.jogador.reiniciar()

        self.turno = 1

        self.jogo_finalizado = False

        self.estado = "ESCOLHENDO_ANIMAL"
    
    def listar_animais(self):

        print("\nAnimais disponíveis:\n")

        for indice, animal in enumerate(self.animais):

            print(f"{indice + 1} - {animal['nome']}")

    def escolher_animal(self, nome):

        for animal in self.animais:

            if animal["nome"] == nome:

                self.jogador.escolher_animal(animal)

                return {

                    "status": "ok"

                }

        return {

            "status": "erro",

            "mensagem": "Animal não encontrado."

        }

    def escolher_animal_jogador(self):

        self.listar_animais()

        while True:

            try:

                opcao = int(
                    input("\nEscolha o número do animal: ")
                )

                if 1 <= opcao <= len(self.animais):
                    break

                print("Opção inválida.")

            except ValueError:

                print("Digite apenas números.")

        animal = self.animais[opcao - 1]

        self.jogador.escolher_animal(animal)
        print(f"\nVocê escolheu: {animal['nome']}")

        self.estado = "VEZ_JOGADOR"
    
    def listar_caracteristicas(self):

        print("\nCaracterísticas disponíveis:\n")

        caracteristicas = list(self.caracteristicas.keys())

        for indice, caracteristica in enumerate(caracteristicas):

            print(f"{indice + 1} - {caracteristica}")

        return caracteristicas
    
    def perguntar_para_ia(self):

        caracteristicas = self.listar_caracteristicas()

        while True:

            try:

                opcao = int(
                    input("\nEscolha uma característica: ")
                )

                if 1 <= opcao <= len(caracteristicas):
                    break

                print("Opção inválida.")

            except ValueError:

                print("Digite apenas números.")

        caracteristica = caracteristicas[opcao - 1]

        self.jogador.adicionar_pergunta(
            caracteristica
        )

        resposta = self.ia.responder(
            caracteristica
        )

        self.jogador.adicionar_historico(
            caracteristica,
            resposta
        )

        print()

        print("IA:")

        print("Sim." if resposta else "Não.")

        return caracteristica, resposta

    def verificar_palpite_jogador(self, animal):

        return self.ia.verificar_palpite(animal)

    def proximo_turno(self):

        self.turno += 1
    
    def rodada_jogador(self):

        caracteristica, resposta = self.perguntar_para_ia()

        return caracteristica, resposta
    
    def rodada_ia(self):

        # Se a IA já descobriu o animal, ela faz um palpite
        if self.ia.pode_adivinhar():

            animal = self.ia.palpite()

            print()
            print("🤖 ACHO QUE DESCOBRI!")
            print()
            print(f"Seu animal é: {animal['nome']}?")

            while True:

                resposta = input("A IA acertou? (s/n): ").lower()

                if resposta in ["s", "sim"]:

                    print()
                    print("🤖 A IA venceu!")
                    self.jogo_finalizado = True
                    return

                if resposta in ["n", "nao", "não"]:

                    print()
                    print("🤔 Então alguma coisa deu errado na lógica.")
                    self.jogo_finalizado = True
                    return

                print("Digite apenas s ou n.")

        self.ia.mostrar_debug()

        # Caso ainda não saiba o animal, continua perguntando
        pergunta = self.ia.escolher_pergunta()

        print()
        print(pergunta_para_texto(pergunta))

        while True:

            resposta = input("Resposta (s/n): ").lower()

            if resposta in ["s", "sim"]:

                resposta = True
                break

            if resposta in ["n", "nao", "não"]:

                resposta = False
                break

            print("Digite apenas s ou n.")

        self.ia.atualizar_animais(
            pergunta,
            resposta
        )

        self.mostrar_resumo_ia()

    def jogar(self):

        self.mostrar_cabecalho()

        self.iniciar()

        print("\n🤖 A IA escolheu um animal.")

        self.escolher_animal_jogador()

        while True:

            self.mostrar_inicio_rodada()

            self.mostrar_vez_jogador()

            self.rodada_jogador()

            self.mostrar_vez_ia()

            self.rodada_ia()

            if self.jogo_finalizado:
                break

            self.proximo_turno()   

    def listar_animais(self):

        return [

            animal["nome"]

            for animal in self.animais

        ]

    def obter_pergunta_investigador(self):

        if self.ia.quantidade_restante() == 0:

            return {

                "tipo": "fim",

                "mensagem": "Não encontrei nenhum animal compatível com as respostas.",

                "encerrado": True,

                "vencedor": False

            }

        # Se já pode dar um palpite
        if self.ia.pode_adivinhar():

            animal = self.ia.palpite()

            return {

                "tipo": "chute",

                "mensagem": f"Acho que seu animal é {animal['nome']}.",

                "encerrado": False

            }

        pergunta = self.ia.escolher_pergunta()

        if pergunta is None:

            return {

                "tipo": "fim",

                "mensagem": "Não consegui formular outra pergunta.",

                "encerrado": True,

                "vencedor": False

            }

        return {

            "tipo": "pergunta",

            "pergunta": self.caracteristicas[pergunta],

            "caracteristica": pergunta,

            "restantes": self.ia.quantidade_restante(),

            "encerrado": False

        }
    
    def responder_investigador(self, caracteristica, mensagem):

        from src.llm.interpretador import interpretar_resposta

        pergunta = self.caracteristicas[caracteristica]

        resposta = interpretar_resposta(
            pergunta,
            mensagem
        )

        self.ia.atualizar_animais(
            caracteristica,
            resposta
        )

        return {

            "restantes": self.ia.quantidade_restante(),

            "encerrado": False

        }
    
    def responder_pergunta_jogador(
        self,
        mensagem
    ):

        caracteristica = interpretar_pergunta(

            mensagem,

            self.caracteristicas

        )

        resposta = self.ia.responder(

            caracteristica

        )

        return {

            "caracteristica": caracteristica,

            "resposta": resposta

        }
    
    def confirmar_chute_investigador(self, correto):

        if correto:

            self.jogo_finalizado = True

            return {

                "vencedor": True,

                "encerrado": True

            }

        animal = self.ia.palpite()

        if animal in self.ia.animais_possiveis:

            self.ia.animais_possiveis.remove(animal)

        return {

            "vencedor": False,

            "encerrado": False

        }
    
    def obter_pergunta_respondedor(self):

        return {

            "tipo": "pergunta",

            "pergunta": "Faça uma pergunta para tentar descobrir meu animal.",

            "encerrado": False

        }