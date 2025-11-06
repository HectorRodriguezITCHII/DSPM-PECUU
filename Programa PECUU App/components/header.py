import flet as ft
import os

class Header(ft.Container):
    """
    Componente de cabecera principal de la aplicación.

    Hereda de ft.Container y está diseñado para ocupar una altura fija (60px) 
    en la parte superior de la página, mostrando elementos clave como el logo,
    el título de la aplicación y el acceso al módulo de usuarios.
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa la cabecera, define sus controles internos y establece el diseño.

        :param page: El objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        """
        super().__init__(height=50)
        
        # --- Lógica de Carga del Logo ---
        # Obtener la ruta absoluta: Asume que la estructura es project_root/src/components/header.py
        # __file__ -> components/header.py
        # os.path.dirname(__file__) -> components/
        # os.path.dirname(os.path.dirname(__file__)) -> project_root/
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_dspm_path = os.path.join(base_dir, "src", "assets", "dspm-logo.png")
        logo_cuu_path = os.path.join(base_dir, "src", "assets", "logo-cuu.png")

        
        self.img_logo_dspm = ft.Image(
            src=logo_dspm_path,
            tooltip="Logo de DSPM",
            fit=ft.ImageFit.CONTAIN,
        )

        self.img_logo_cuu = ft.Image(
            src=logo_cuu_path,
            tooltip="Logo del Municipio de Chihuahua",
            fit=ft.ImageFit.CONTAIN,
        )
        
        # --- Diseño de la Cabecera ---
        # Utiliza un ft.Row para alinear el logo, el título y el botón.
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Distribuye los elementos en los extremos
            controls=[
                self.img_logo_dspm,
                ft.Text(
                    value="SISTEMA DE GESTIÓN DE CÁMARAS CIUDADANAS",
                    size=24,
                    color=ft.Colors.INDIGO_900,
                    weight="bold"
                ),
                self.img_logo_cuu,
            ]
        )