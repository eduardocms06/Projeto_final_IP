import flet as ft

def botao_voltar(page: ft.Page, rota_destino: str) -> ft.Container:
    def ao_clicar(_):
        page.go(rota_destino)

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon("arrow_back_ios", color="#F3BD0A", size=18),
                ft.Text(value="VOLTAR", font_family="MILKER", color="#F3BD0A", size=16)
            ],
            spacing=6,
            tight=True
        ),
        on_click=ao_clicar,
        padding=ft.Padding.only(left=20, top=20, right=10, bottom=10),
        ink=True,
    )