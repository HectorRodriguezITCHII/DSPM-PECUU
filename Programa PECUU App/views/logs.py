import flet as ft

class Logs(ft.Container):
    """
    Representa la vista de "Logs" de la aplicación.

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

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._create_header(),
            ]
        )

    def _create_header(self):
        """
        Crea y retorna el contenedor que actúa como cabecera o título de la vista.

        :returns: Un objeto ft.Container que contiene el título y un divisor.
        :rtype: ft.Container
        """
        return ft.Container(
            padding=ft.padding.only(bottom=20),
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.HISTORY, size=30, color=ft.Colors.AMBER),
                            ft.Text(
                                value="HISTORIAL DE CAMBIOS",
                                size=26,
                                color=ft.Colors.INDIGO_500,
                                weight="bold"
                            )
                        ],
                        spacing=10
                    ),
                    ft.Divider(height=10, color=ft.Colors.GREY_300)
                ]
            )
        )