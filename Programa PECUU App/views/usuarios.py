import flet as ft
from components.inner_header import InnerHeader

class Usuarios(ft.Container):
    """
    Representa la vista de "Usuarios" de la aplicación.

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

        self.user_icon = ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=150, color=ft.Colors.GREY_500)
        self.user_firstname = ft.Text("[Nombre]", size=16, color=ft.Colors.GREY_800)
        self.user_lastname = ft.Text("[Apellido]", size=16, color=ft.Colors.GREY_800)
        self.user_id = ft.Text("ID: [000000]", size=16, color=ft.Colors.GREY_800)
        self.edit_button = ft.ElevatedButton("Editar Usuario", icon=ft.Icons.EDIT)

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("USUARIOS", icon=ft.Icons.ACCOUNT_BOX),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=50,
                    controls=[
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                self.user_icon,
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Nombre:", size=20, color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD),
                            self.user_firstname,
                            ft.Text("Apellido:", size=20, color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD),
                            self.user_lastname,
                            ft.Text("ID de Usuario:", size=20, color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD),
                            self.user_id,
                        ]
                    )]
                ),
                self.edit_button
            ]
        )