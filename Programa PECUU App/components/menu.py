import flet as ft

class Menu(ft.NavigationBar):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.bgcolor=ft.Colors.GREY_50
        self.destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.WIFI_TETHERING_OUTLINED,
                selected_icon=ft.Icons.WIFI_TETHERING,
                label="Escaneo General",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.ROUTER_OUTLINED,
                selected_icon=ft.Icons.ROUTER,
                label="Escaneo Local",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Inicio",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.HUB_OUTLINED,
                selected_icon=ft.Icons.HUB,
                label="Enlaces",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.HISTORY_OUTLINED,
                selected_icon=ft.Icons.HISTORY,
                label="Historial",
            ),
        ]