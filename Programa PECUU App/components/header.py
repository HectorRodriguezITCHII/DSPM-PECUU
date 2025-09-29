import flet as ft

img_logo_white = ft.Image(
        src="/dspm-logo-white.png",
        tooltip="Logo de DSPM",
    )

class Header(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(height=60)
        self.bgcolor=ft.Colors.INDIGO_500,
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                img_logo_white,
                ft.Text(
                    value="SISTEMA DE GESTIÓN DE CÁMARAS CIUDADANAS",
                    size=26,
                    color=ft.Colors.WHITE,
                    weight="bold"
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.ACCOUNT_CIRCLE, icon_color=ft.Colors.WHITE, icon_size=30, tooltip="Usuarios"),
                        ft.IconButton(ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE, icon_size=30, tooltip="Configuración")
                    ]
                )
            ]
        )