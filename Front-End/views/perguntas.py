import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
from components.botao_voltar import botao_voltar

def view_perguntas(page: ft.Page, modalidade_id: str) -> ft.View:
    """
    Tela de perguntas e respostas.
    Por enquanto exibe apenas a estrutura visual da interface.
    A lógica de perguntas/respostas será adicionada futuramente.
    """

    titulo = ft.Text(
        value=f"MODALIDADE {modalidade_id}",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#F3BD0A",
        font_family="AKIRA",
        style=ft.TextStyle(
            shadow=[ft.BoxShadow(color="#F3BD0A", offset=ft.Offset(0, 0), blur_radius=10)]
        )
    )

    contador = ft.Text(
        value="1 / 10",
        size=16,
        color="#888888",
        font_family="MILKER"
    )

    caixa_pergunta = ft.Container(
        content=ft.Text(
            value="A pergunta aparecerá aqui...",
            size=26,
            color="#FFFFFF",
            font_family="MILKER",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.Alignment(0, 0),
        width=800,
        padding=30,
        border_radius=12,
        border=ft.Border.all(2, "#251f38"),
    )

    caixa_resposta = ft.Container(
        content=ft.Text(
            value="A resposta aparecerá aqui...",
            size=22,
            color="#F3BD0A",
            font_family="MILKER",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.Alignment(0, 0),
        width=800,
        padding=30,
        border_radius=12,
        border=ft.Border.all(2, "#F3BD0A"),
    )

    btn_resposta = ft.Container(
        content=ft.Text(value="VER RESPOSTA", font_family="MILKER", color="#F3BD0A", size=20),
        alignment=ft.Alignment(0, 0),
        width=280,
        height=50,
        border_radius=10,
        border=ft.Border.all(2, "#251f38"),
    )

    btn_proxima = ft.Container(
        content=ft.Text(value="PRÓXIMA", font_family="MILKER", color="#FFFFFF", size=20),
        alignment=ft.Alignment(0, 0),
        width=280,
        height=50,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#8a2be2", "#da70d6"]
        ),
        shadow=ft.BoxShadow(blur_radius=15, color="#da70d6", offset=ft.Offset(0, 0)),
    )

    conteudo = ft.Column(
        controls=[
            titulo,
            ft.Container(height=10),
            contador,
            ft.Container(height=30),
            caixa_pergunta,
            ft.Container(height=20),
            caixa_resposta,
            ft.Container(height=30),
            ft.Row(
                controls=[btn_resposta, btn_proxima],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    return ft.View(
        route=f"/perguntas/{modalidade_id}",
        controls=[
            ft.Stack(
                controls=[
                    ft.Container(content=conteudo, expand=True),
                    ft.Container(
                        content=botao_voltar(page, "/modalidades"),
                        top=0,
                        left=0
                    )
                ],
                expand=True
            )
        ],
        bgcolor="#0A0919",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=0
    )