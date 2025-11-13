import flet as ft
from components.inner_header import InnerHeader
from views.enlaces_añadir import EnlacesAñadir

class Enlaces(ft.Container):
    """
    Representa la vista de "Enlaces" de la aplicación.

    Hereda de ft.Container y se configura para ocupar toda el área de contenido
    principal de la aplicación.
    """
    def __init__(self, page: ft.Page, change_view=None):
        """
        Inicializa la vista y configura todos los componentes de la interfaz.

        :param page: Objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        :param change_view: Función callback para cambiar de vista.
        :type change_view: callable
        """
        super().__init__()
        self.page = page
        self.change_view = change_view
        # Configuración del contenedor principal de la vista
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        self.add_button = ft.FilledButton(
            "Añadir", 
            icon=ft.Icons.ADD, 
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            width=150,
            height=50,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=20), icon_size=30),
            on_click=lambda e: self.change_view("enlaces_añadir") if self.change_view else None
        )

        self.delete_button = ft.FilledButton(
            "Eliminar", 
            icon=ft.Icons.DELETE, 
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE,
            width=150,
            height=50,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=20), icon_size=30)
        )

        # --- Botones de Acción ---
        self.inspect_button = ft.IconButton(
            icon=ft.Icons.VISIBILITY,
            icon_color=ft.Colors.INDIGO_ACCENT_400,
            tooltip="Inspeccionar"
        )
        
        # --- Estilo de Texto para las Celdas de la Tabla ---
        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.GREY_800
        )

        # --- Tabla de Datos (ft.DataTable) ---
        self.data_table = ft.DataTable(
            expand=True,
            horizontal_lines=ft.border.BorderSide(1, color=ft.Colors.GREY_300),
            columns=[
                ft.DataColumn(ft.Text(""), ),
                ft.DataColumn(ft.Text("Nombre", style=self.text_style)),
                ft.DataColumn(ft.Text("DDNS", style=self.text_style)),
                ft.DataColumn(ft.Text("Puerto HTTP", style=self.text_style), numeric=True),
                ft.DataColumn(ft.Text("Puerto RTSP", style=self.text_style), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(self.inspect_button),
                        ft.DataCell(ft.Text("Escuela Pública", style=self.text_style)),
                        ft.DataCell(ft.Text("Escuela1.ddns.net", style=self.text_style)),
                        ft.DataCell(ft.Text("80", style=self.text_style)),
                        ft.DataCell(ft.Text("554", style=self.text_style)),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(self.inspect_button),
                        ft.DataCell(ft.Text("Plaza Central", style=self.text_style)),
                        ft.DataCell(ft.Text("PlazaCentral.ddns.net", style=self.text_style)),
                        ft.DataCell(ft.Text("80", style=self.text_style)),
                        ft.DataCell(ft.Text("1024", style=self.text_style)),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(self.inspect_button),
                        ft.DataCell(ft.Text("Parque Norte", style=self.text_style)),
                        ft.DataCell(ft.Text("ParqueNorte.ddns.net", style=self.text_style)),
                        ft.DataCell(ft.Text("81", style=self.text_style)),
                        ft.DataCell(ft.Text("1024", style=self.text_style)),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(self.inspect_button),
                        ft.DataCell(ft.Text("Fraccionamiento", style=self.text_style)),
                        ft.DataCell(ft.Text("Fraccionamiento.ddns.net", style=self.text_style)),
                        ft.DataCell(ft.Text("82", style=self.text_style)),
                        ft.DataCell(ft.Text("1024", style=self.text_style)),
                    ],
                ),
            ],
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("ENLACES", icon=ft.Icons.HUB),
                # La tabla de datos dentro de una fila para que
                # pueda abarcar toda la pantalla horizontalmente
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[self.add_button, self.delete_button]
                ),
                ft.Row(
                    controls=[self.data_table]
                ),
                
            ]
        )