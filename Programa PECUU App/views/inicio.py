import flet as ft
from components.inner_header import InnerHeader

class Inicio(ft.Container):
    """
    Representa la vista de "Inicio" de la aplicación.
    
    Hereda de ft.Container y se configura para ocupar toda el área de contenido 
    principal de la aplicación.
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa la vista y configura todos los componentes de la interfaz.

        :param page: Objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        """
        super().__init__()
        # Configuración del contenedor principal de la vista
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        self.activity_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ASSIGNMENT),
                        title=ft.Text("Actividad de hoy", weight="bold", size=20),
                        subtitle=ft.Text(
                            "Descripción de la actividad."
                        ),
                        bgcolor=ft.Colors.GREY_400,
                    ),
                    ft.Row(
                        [ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.INDIGO_ACCENT), ft.IconButton(ft.Icons.CHECK, icon_color=ft.Colors.GREEN)],
                        alignment=ft.MainAxisAlignment.END,
                    )]
                ),
                width=400,
                padding=10,
            ),
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("ACTIVIDADES", icon=ft.Icons.HOME),
                self.activity_card,
            ]
        )