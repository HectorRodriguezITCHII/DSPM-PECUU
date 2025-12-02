import flet as ft

class InnerHeader(ft.Container):
    """
    Componente de cabecera secundario de las vistas.

    Muestra el título de la vista actual con un icono personalizable.
    """
    def __init__(self, title: str, icon: str = ft.Icons.CIRCLE):
        """
        Inicializa la cabecera, define sus controles internos y establece el diseño.

        :param title: El título de la vista a mostrar.
        :type title: str
        :param icon: El icono a mostrar junto al título (por defecto ft.Icons.CIRCLE).
        :type icon: str
        """
        super().__init__()

        self.title_text = ft.Text(
            value=title,
            size=26,
            color=ft.Colors.INDIGO_500,
            weight="bold"
        )
        
        # --- Diseño de la Cabecera ---
        # Utiliza un ft.Row para alinear el icono y el título.
        self.content = ft.Container(
            padding=ft.padding.only(bottom=10),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon, size=30, color=ft.Colors.AMBER),
                            self.title_text
                        ],
                        spacing=10
                    ),
                    ft.Divider(height=10, color=ft.Colors.GREY_300)
                ]
            )
        )