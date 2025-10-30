import flet as ft
import os

class Header(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(height=60)
        
        self.usuarios_btn = ft.IconButton(
            icon=ft.Icons.ACCOUNT_CIRCLE,
            icon_color=ft.Colors.INDIGO_500,
            icon_size=40,
            tooltip="Usuarios"
        )
        
        # Obtener ruta absoluta de la imagen
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "src", "assets", "dspm-logo.png")
        
        self.img_logo = ft.Image(
            src=logo_path,
            tooltip="Logo de DSPM",
            fit=ft.ImageFit.CONTAIN,
        )
        
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.img_logo,
                ft.Text(
                    value="SISTEMA DE GESTIÓN DE CÁMARAS CIUDADANAS",
                    size=26,
                    color=ft.Colors.INDIGO_900,
                    weight="bold"
                ),
                self.usuarios_btn,
            ]
        )