import flet as ft
from components.inner_header import InnerHeader
from components.enlaces import EnlacesManager
from views.enlaces_agregar import EnlacesAgregar
from services.api_service import ApiService

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
        
        # Cargar datos desde la API
        self.load_enlaces_from_api()
    
    def add_enlace(self, enlace_data):
        """Delegar en EnlacesManager para añadir un enlace."""
        EnlacesManager.add_enlace(self, enlace_data)
    
    def delete_row(self, e, enlace_data):
        """Delegar en EnlacesManager para eliminar una fila."""
        EnlacesManager.delete_row(self, enlace_data)
    
    def load_enlaces_from_api(self):
        """
        Carga los enlaces desde la API y los muestra en la tabla.
        Este método se llama cuando se inicializa la vista.
        """
        try:
            enlaces = ApiService.get_links()
            if enlaces:
                # Limpiar la tabla actual
                self.data_table.rows.clear()
                
                # Agregar cada enlace a la tabla
                for enlace in enlaces:
                    EnlacesManager.add_enlace(self, enlace)
                
                print(f"Se cargaron {len(enlaces)} enlaces desde la API")
            else:
                print("No se pudieron obtener los enlaces desde la API")
        except Exception as e:
            print(f"Error al cargar enlaces desde la API: {e}")
    
    def refresh_enlaces_from_api(self):
        """
        Refresca los enlaces desde la API.
        Puede ser llamado por un botón de actualización.
        """
        self.load_enlaces_from_api()
        if self.page:
            self.page.update()