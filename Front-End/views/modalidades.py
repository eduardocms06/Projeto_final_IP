import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
from components.botao_voltar import botao_voltar

# Defina aqui os nomes reais das suas modalidades
MODALIDADES = [
    {"id": "1", "nome": "MODALIDADE 1", "cores": ["#8a2be2", "#da70d6"], "glow": "#da70d6"},
    {"id": "2", "nome": "MODALIDADE 2", "cores": ["#1a6dff", "#00c6ff"], "glow": "#00c6ff"},
    {"id": "3", "nome": "MODALIDADE 3", "cores": ["#ff4e00", "#ff9000"], "glow": "#ff9000"},
    {"id": "4", "nome": "MODALIDADE 4", "cores": ["#00b09b", "#96c93d"], "glow": "#96c93d"},
    {"id": "5", "nome": "MODALIDADE 5", "cores": ["#c94b4b", "#4b134f"], "glow": "#c94b4b"},
    {"id": "6", "nome": "MODALIDADE 6", "cores": ["#f7971e", "#ffd200"], "glow": "#ffd200"},
]

def _botao_modalidade(page: ft.Page, modalidade: dict) -> ft.Container:
    """Cria um botão estilizado para cada modalidade."""
    return ft.Container(
        content=ft.Stack(
            controls=[
                ft.Text(
                    value=modalidade["nome"],
                    font_family="MILKER",
                    size=22,
                    style=ft.TextStyle(
                        foreground=ft.Paint(
                            color="#000000",
                            stroke_width=3,
                            style=ft.PaintingStyle.STROKE
                        )
                    )
                ),
                ft.Text(value=modalidade["nome"], font_family="MILKER", color="#FFFFFF", size=22)
            ],
            alignment=ft.Alignment(0, 0)
        ),
        alignment=ft.Alignment(0, 0),
        width=280,
        height=60,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=modalidade["cores"]
        ),
        shadow=ft.BoxShadow(blur_radius=15, color=modalidade["glow"], offset=ft.Offset(0, 0)),
        on_click=lambda _, mid=modalidade["id"]: page.go(f"/perguntas/{mid}")
    )

def view_modalidades(page: ft.Page) -> ft.View:
    """
    Tela de seleção de modalidades.
    Exibe 6 botões organizados em grade 2x3.
    Possui botão voltar para o menu principal.
    """

    titulo = ft.Text(
        value="MODALIDADES",
        size=45,
        weight=ft.FontWeight.BOLD,
        color="#F3BD0A",
        font_family="AKIRA",
        style=ft.TextStyle(
            shadow=[ft.BoxShadow(color="#F3BD0A", offset=ft.Offset(0, 0), blur_radius=10)]
        )
    )

    # Grade 2x3 com os 6 botões
    grade_botoes = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    _botao_modalidade(page, MODALIDADES[0]),
                    _botao_modalidade(page, MODALIDADES[1]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ),
            ft.Row(
                controls=[
                    _botao_modalidade(page, MODALIDADES[2]),
                    _botao_modalidade(page, MODALIDADES[3]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ),
            ft.Row(
                controls=[
                    _botao_modalidade(page, MODALIDADES[4]),
                    _botao_modalidade(page, MODALIDADES[5]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    conteudo = ft.Column(
        controls=[
            titulo,
            ft.Container(height=40),
            grade_botoes
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    return ft.View(
        route="/modalidades",
        controls=[
            ft.Stack(
                controls=[
                    # Conteúdo centralizado
                    ft.Container(content=conteudo, expand=True),
                    # Botão voltar fixo no canto superior esquerdo
                    ft.Container(
                        content=botao_voltar(page, "/"),
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