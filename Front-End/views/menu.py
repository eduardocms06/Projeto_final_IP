import flet as ft

def view_menu(page: ft.Page) -> ft.View:
    """
    Tela inicial do app.
    Contém os botões: Modalidades e Sair.
    Não possui botão voltar pois é a tela raiz.
    """

    titulo = ft.Text(
        value="QUEM SOU EU?",
        size=50,
        weight=ft.FontWeight.BOLD,
        color="#F3BD0A",
        font_family="AKIRA",
        style=ft.TextStyle(
            shadow=[
                ft.BoxShadow(
                    color="#F3BD0A",
                    offset=ft.Offset(0, 0),
                    blur_radius=10,
                )
            ]
        )
    )

    button_modalidades = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Text(
                    value="MODALIDADES",
                    font_family="MILKER",
                    size=30,
                    style=ft.TextStyle(
                        foreground=ft.Paint(
                            color="#000000",
                            stroke_width=3,
                            style=ft.PaintingStyle.STROKE
                        )
                    )
                ),
                ft.Text(value="MODALIDADES", font_family="MILKER", color="#FFFFFF", size=30)
            ],
            alignment=ft.Alignment(0, 0)
        ),
        alignment=ft.Alignment(0, 0),
        width=300,
        height=50,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#8a2be2", "#da70d6"]
        ),
        shadow=ft.BoxShadow(blur_radius=15, color="#da70d6", offset=ft.Offset(0, 0)),
        on_click=lambda _: page.go("/modalidades")
    )
    async def sair_click():
        await page.window.close()
    button_sair = ft.Container(
        content=ft.Text(value="SAIR", size=30, font_family="MILKER", color="#dbdbdb"),
        alignment=ft.Alignment(0, 0),
        width=300,
        height=50,
        border_radius=10,
        border=ft.Border.all(2, "#251f38"),
        on_click=sair_click
    )

    botoes = ft.Row(
        controls=[button_modalidades, button_sair],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30
    )

    conteudo = ft.Column(
        controls=[titulo, ft.Container(height=30), botoes],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    return ft.View(
        route="/",
        controls=[conteudo],
        bgcolor="#0A0919",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=0
    )