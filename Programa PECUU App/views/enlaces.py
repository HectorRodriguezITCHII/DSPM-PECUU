import flet as ft
from components.inner_header import InnerHeader
from views.enlaces_agregar import EnlacesAgregar

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
            on_click=lambda e: self.change_view("enlaces_agregar") if self.change_view else None
        )

        # --- Botones de Acción ---
        self.inspect_button = ft.IconButton(
            icon=ft.Icons.VISIBILITY,
            icon_color=ft.Colors.INDIGO_ACCENT_400,
            tooltip="Inspeccionar"
        )
        
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_ACCENT_400,
            tooltip="Eliminar"
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
                ft.DataColumn(ft.Text(""), ),
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
                    controls=[self.add_button]
                ),
                ft.Row(
                    controls=[self.data_table]
                ),
                
            ]
        )
    
    def add_enlace(self, enlace_data):
        """
        Agrega una nueva fila a la tabla de enlaces.
        
        :param enlace_data: Diccionario con los datos del enlace.
        :type enlace_data: dict
        """
        # Crear botones de acción para la nueva fila
        inspect_btn = ft.IconButton(
            icon=ft.Icons.VISIBILITY,
            icon_color=ft.Colors.INDIGO_ACCENT_400,
            tooltip="Inspeccionar"
        )
        
        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_ACCENT_400,
            tooltip="Eliminar",
            on_click=lambda e: self.delete_row(e, enlace_data)
        )
        
        # Crear nueva fila
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(inspect_btn),
                ft.DataCell(ft.Text(enlace_data["nombre"], style=self.text_style)),
                ft.DataCell(ft.Text(enlace_data["ddns"], style=self.text_style)),
                ft.DataCell(ft.Text(enlace_data["puerto_http"], style=self.text_style)),
                ft.DataCell(ft.Text(enlace_data["puerto_rtsp"], style=self.text_style)),
                ft.DataCell(delete_btn),
            ]
        )
        
        # Agregar la fila a la tabla
        self.data_table.rows.append(new_row)
        self.page.update()
    
    def delete_row(self, e, enlace_data):
        """
        Elimina una fila de la tabla de enlaces.
        
        :param e: Evento de clic.
        :param enlace_data: Datos del enlace a eliminar.
        """
        # Buscar y eliminar la fila
        for row in self.data_table.rows:
            if row.cells[1].content.value == enlace_data["nombre"]:
                self.data_table.rows.remove(row)
                self.page.update()
                break