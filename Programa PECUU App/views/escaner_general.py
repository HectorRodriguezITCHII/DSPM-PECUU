import flet as ft
from components.escaner_general import scan_urls_handler, last_excel_file
from components.inner_header import InnerHeader
import webbrowser
import os

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

        # --- Botón de Abrir Excel ---
        self.download_button = ft.FilledButton(
            text="ABRIR EXCEL",
            width=200,
            height=40,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.OPEN_IN_BROWSER,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight="bold"), icon_size=26),
            disabled=True,
            visible=False
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
                self.download_button,
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
            self.download_button
        )
        
        # Evento del botón de descarga
        self.download_button.on_click = self.download_excel
    
    def download_excel(self, e):
        """
        Abre el archivo Excel generado en el explorador de archivos
        o lo descarga dependiendo del sistema operativo.
        """
        import components.escaner_general as scanner_module
        
        if scanner_module.last_excel_file and os.path.exists(scanner_module.last_excel_file):
            try:
                # Abre el explorador de archivos con el archivo seleccionado
                if os.name == 'nt':  # Windows
                    os.startfile(scanner_module.last_excel_file)
                else:  # macOS o Linux
                    os.system(f'open "{scanner_module.last_excel_file}"')
                print(f"[INFO] Abriendo archivo: {scanner_module.last_excel_file}")
            except Exception as ex:
                print(f"[ERROR] No se pudo abrir el archivo: {str(ex)}")
        else:
            print("[ERROR] No hay archivo Excel disponible para descargar")