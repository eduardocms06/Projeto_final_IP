import flet as ft
def inicio(page: ft.Page):
    page.title = "WHO I AM?"
    page.bgcolor = "#1E1961"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER    #Alinhamento no centro horizontal
    page.vertical_alignment = ft.MainAxisAlignment.CENTER       #Alinhamento no centro vertical
    page.window_width = 1920        #Define o largura da janela
    page.window_height = 1080       #Define o altura da janela

    #título
    titulo = ft.Text(
        value = "QUEM SOU EU?",
        size = 50,
        weight = ft.FontWeight.BOLD,
        color = "#F3BD0A"
    )

    inicio()