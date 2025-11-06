import flet as ft
from components.escaner_general import scan_urls_handler 
from components.inner_header import InnerHeader

class EscanerGeneral(ft.Container):
    """
    Representa la vista de "Escaner General" de la aplicación.
    
    Es un contenedor de Flet que contiene el botón principal de escaneo,
    indicadores de carga y un área para mostrar los resultados del escaneo
    de URLs.

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
        
        # --- Componentes de la Barra de Carga ---
        self.loading_indicator = ft.ProgressRing(
            width=30, 
            height=30, 
            stroke_width=4, 
            color=ft.Colors.AMBER
        )
        
        self.status_text = ft.Text(
            value="",
            size=20
        )

        # --- Botón de Escaneo Principal ---
        self.scan_button = ft.FilledButton(
            text="ESCANEAR",
            width=150,
            height=150,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=22, weight="bold")),
        )

        # --- Área de Resultados ---
        # Columna donde se insertarán dinámicamente los ft.Card con los resultados
        self.results_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # --- Indicador de Carga Agrupado ---
        self.loading_row = ft.Row(
            controls=[self.loading_indicator, self.status_text],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False  # Inicialmente oculto
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("ESCANEO GENERAL", icon=ft.Icons.WIFI_TETHERING),
                self.scan_button,
                self.results_column,
                self.loading_row
            ]
        )

        # --- Conexión del Evento de Clic ---
        # Al hacer clic, llama a la función externa 'scan_urls_handler' 
        # y le pasa las referencias de los controles que debe actualizar.
        self.scan_button.on_click = lambda e: scan_urls_handler(
            e,
            self.results_column,
            self.loading_row,
            self.scan_button,
            page,
        )