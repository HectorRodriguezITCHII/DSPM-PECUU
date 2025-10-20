import flet as ft

class Menu(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(width=60, border_radius=10, padding=5)
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.INDIGO_50, ft.Colors.INDIGO_600],
        )

        #guardar los iconos como atributos
        self.inicio_btn = ft.IconButton(icon=ft.Icons.HOME_OUTLINED, tooltip="Inicio", icon_color=ft.Colors.INDIGO_500)
        self.escaner_general_btn = ft.IconButton(icon=ft.Icons.WIFI_TETHERING_OUTLINED, tooltip="Escaneo General", icon_color=ft.Colors.INDIGO_400)
        self.escaner_local_btn = ft.IconButton(icon=ft.Icons.ROUTER_OUTLINED, tooltip="Escaneo Local", icon_color=ft.Colors.INDIGO_400)
        self.enlaces_btn = ft.IconButton(icon=ft.Icons.HUB_OUTLINED, tooltip="Enlaces", icon_color=ft.Colors.INDIGO_400)
        self.historial_btn = ft.IconButton(icon=ft.Icons.HISTORY_OUTLINED, tooltip="Historial", icon_color=ft.Colors.INDIGO_400)
        self.ajustes_btn = ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Ajustes", icon_color=ft.Colors.INDIGO_50)

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    controls=[
                        self.inicio_btn,
                        self.escaner_general_btn,
                        self.escaner_local_btn,
                        self.enlaces_btn,
                        self.historial_btn,
                    ]
                ),  
                ft.Column(
                    controls=[
                        self.ajustes_btn,
                    ]
                ),
            ]
        )