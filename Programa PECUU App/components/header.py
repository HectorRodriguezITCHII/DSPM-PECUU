import flet as ft

# La carpeta de assets se servirá con assets_dir, por lo que aquí solo referimos el nombre del archivo
img_logo_white = ft.Image(
        src="dspm-logo.png",
        tooltip="Logo de DSPM",
    )

class Header(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(height=60)
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                img_logo_white,
                ft.Text(
                    value="SISTEMA DE GESTIÓN DE CÁMARAS CIUDADANAS",
                    size=26,
                    color=ft.Colors.INDIGO_500,
                    weight="bold"
                ),
                ft.IconButton(icon=ft.Icons.ACCOUNT_CIRCLE, icon_color=ft.Colors.INDIGO_500, icon_size=30, tooltip="Usuarios"),
            ]
        )