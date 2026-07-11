class Jogador:

    def __init__(self):

        self.animal = None

        self.historico = []

    def escolher_animal(self, animal):

        self.animal = animal

    def responder(self, caracteristica):

        return self.animal.get(
            caracteristica,
            False
        )

    def adicionar_historico(self, caracteristica, resposta):

        self.historico.append({

            "caracteristica": caracteristica,

            "resposta": resposta

        })

    def reiniciar(self):

        self.animal = None

        self.historico = []