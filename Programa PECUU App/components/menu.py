import flet as ft

class Menu(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(width=60, border_radius=10, padding=5)
        self.bgcolor=ft.Colors.GREY_50
        
        #guardar los iconos como atributos
        self.inicio_btn = ft.IconButton(icon=ft.icons.HOME_OUTLINED, tooltip="Inicio", icon_color=ft.Colors.BLUE_400)
        self.escaner_general_btn = ft.IconButton(icon=ft.icons.WIFI_TETHERING_OUTLINED, tooltip="Escaneo General", icon_color=ft.Colors.BLUE_400)
        self.escaner_local_btn = ft.IconButton(icon=ft.icons.ROUTER_OUTLINED, tooltip="Escaneo Local", icon_color=ft.Colors.BLUE_400)
        self.enlaces_btn = ft.IconButton(icon=ft.icons.HUB_OUTLINED, tooltip="Enlaces", icon_color=ft.Colors.BLUE_400)
        self.historial_btn = ft.IconButton(icon=ft.icons.HISTORY_OUTLINED, tooltip="Historial", icon_color=ft.Colors.BLUE_400)
        
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.inicio_btn,
                self.escaner_general_btn,
                self.escaner_local_btn,
                self.enlaces_btn,
                self.historial_btn,
            ]
        )