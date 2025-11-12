import flet as ft
from components.inner_header import InnerHeader

class Actividades(ft.Container):
    """
    Representa la vista de "Actividades" de la aplicación.

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
                        leading=ft.Icon(ft.Icons.ASSIGNMENT, ft.Colors.INDIGO_ACCENT_400),
                        title=ft.Text("Actividad de hoy", weight="bold", size=20, color=ft.Colors.GREY_800),
                        subtitle=ft.Text("[Usuario]", color=ft.Colors.GREY_600),
                        trailing=ft.Text("12:00 PM", color=ft.Colors.GREY_600),
                    ),
                    ft.Text("Descripción de la actividad.", color=ft.Colors.GREY_600),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                        ft.IconButton(ft.Icons.CHECK, icon_color=ft.Colors.GREEN),
                        ft.PopupMenuButton(items=[
                            ft.PopupMenuItem(text="Editar"),
                            ft.PopupMenuItem(text="Eliminar"),
                        ],
                        tooltip="Opciones",
                        )
                    ]),
                ]),
                width=400,
                padding=10,
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
            )
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