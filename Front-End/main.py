import flet as ft
from views.menu import view_menu
from views.modalidades import view_modalidades
from views.perguntas import view_perguntas

def main(page: ft.Page):
    page.fonts = {
        "AKIRA": "AKIRA EXPANDED DEMO.otf",
        "MILKER": "MILKER.otf"
    }

    page.title = "WHO I AM?"
    page.bgcolor = "#0A0919"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1920
    page.window.height = 1080

    def route_change(e):
        print(f"Rota atual: {page.route}")   # Debug — aparece no terminal
        page.views.clear()

        if page.route == "/":
            page.views.append(view_menu(page))

        elif page.route == "/modalidades":
            page.views.append(view_modalidades(page))

        elif page.route.startswith("/perguntas/"):
            modalidade_id = page.route.split("/")[-1]
            page.views.append(view_perguntas(page, modalidade_id))

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.route = top_view.route
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.route = "/"
    route_change(None)

ft.run(main, assets_dir="Front-End/assets")