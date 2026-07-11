PERGUNTAS = {
    "mamifero": "O seu animal é mamífero?",
    "anfibio": "O seu animal é um anfíbio?",
    "reptil": "O seu animal é um réptil?",
    "ave": "O seu animal é uma ave?",
    "peixe": "O seu animal é um peixe?",
    "inseto": "O seu animal é um inseto?",

    "voa": "O seu animal voa?",
    "nada": "O seu animal nada?",
    "salta": "O seu animal salta?",
    "escala_arvores": "O seu animal escala árvores?",

    "vive_floresta": "O seu animal vive na floresta?",
    "vive_deserto": "O seu animal vive no deserto?",
    "vive_agua": "O seu animal vive na água?",
    "vive_oceano": "O seu animal vive no oceano?",
    "vive_america_sul": "O seu animal vive na América do Sul?",

    "e_carnivoro": "O seu animal é carnívoro?",
    "e_herbivoro": "O seu animal é herbívoro?",
    "e_noturno": "O seu animal é noturno?",
    "e_venenoso": "O seu animal é venenoso?",

    "porte_pequeno": "O seu animal é de pequeno porte?",
    "porte_grande": "O seu animal é de grande porte?",

    "tem_listras_ou_manchas": "O seu animal possui listras ou manchas?",
    "cor_colorida": "O seu animal possui cores chamativas?"
}


def pergunta_para_texto(caracteristica):

    return PERGUNTAS.get(
        caracteristica,
        caracteristica.replace("_", " ").capitalize() + "?"
    )