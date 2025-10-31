import flet as ft
from components.escaner_local import NetworkScanner

class EscanerLocal(ft.Container):
    """
    Representa la vista de "Escaneo Local" de la aplicación.
    
    Esta vista permite al usuario ver su información de red (IP LAN/WAN) 
    e iniciar un escaneo de puertos, ya sea a su propia IP pública o 
    a una IP personalizada ingresada en el campo de texto.

    Hereda de ft.Container y se utiliza como un panel en la interfaz principal.
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa la vista, obtiene la información de red e instancia 
        todos los componentes de la interfaz de Flet.

        :param page: Objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        """
        super().__init__()
        # Configuración visual del contenedor principal de la vista
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        # --- Indicadores de Carga y Estado ---
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
        
        # --- Inicialización del Escáner y Datos de Red ---
        # Crea la instancia del motor de escaneo y obtiene las IPs al inicio.
        self.scanner = NetworkScanner()

        self.info_text = ft.Text(
            value="INFORMACIÓN DE LA RED:",
            size=22,
            color=ft.Colors.GREY_700,
            weight="bold"
        )

        self.info_lan_text = ft.Text(
            value="IP Local (LAN): " + (self.scanner.lan_ip or "N/D"),
            size=18,
            color=ft.Colors.GREY_700,
        )

        self.info_wan_text = ft.Text(
            value="IP Pública (WAN): " + (self.scanner.wan_ip or "N/D"),
            size=18,
            color=ft.Colors.GREY_700,
        )

        # Contenedor que agrupa la información de red
        self.info_container = ft.Container(
            padding=ft.padding.all(15),
            border_radius=10,
            margin=ft.margin.only(bottom=20),
            width=400,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.info_text,
                    self.info_lan_text,
                    self.info_wan_text,
                ]
            )
        )

        # --- Controles de Escaneo ---
        # Botón para escanear la IP WAN obtenida automáticamente.
        self.scan_button = ft.FilledButton(
            text="ESCANEAR " + (self.scanner.wan_ip or "IP PÚBLICA"),
            width=300,
            height=50,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, weight="bold")),
        )

        # Campo de texto para ingresar una IP de escaneo personalizada.
        self.ip_textfield = ft.TextField(
            width=240,
            height=50,
            hint_text="O escanear otra IP...",
            text_style=ft.TextStyle(size=16, color=ft.Colors.GREY_700),
            border_color=ft.Colors.GREY_300,
            border_radius=10
        )

        # Botón para iniciar escaneo de la IP ingresada.
        self.scan_ip_button = ft.IconButton(
            icon=ft.Icons.WIFI_TETHERING,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.INDIGO_500,
            width=50, height=50,
            hover_color=ft.Colors.INDIGO_400
        )

        # Fila que contiene el campo de texto y el botón de escaneo de IP personalizada
        self.ingresar_ip_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.ip_textfield,
                self.scan_ip_button
            ]
        )

        # Contenedor que agrupa las opciones de escaneo
        self.buttons_container = ft.Container(
            margin=ft.margin.only(bottom=20),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.scan_button, self.ingresar_ip_row]
            )
        )

        # Fila para mostrar el indicador de carga y el texto de estado (oculto por defecto)
        self.loading_row = ft.Row(
            controls=[self.loading_indicator, self.status_text],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )

        # Columna donde se mostrarán los resultados del escaneo (puertos abiertos)
        self.results_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # --- Contenedor Principal (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._create_header(),
                self.info_container,
                self.buttons_container,
                self.loading_row,
                # Contenedor visual para los resultados
                ft.Container(
                    content=self.results_column,
                    width=300,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    border_radius=10,
                    padding=ft.padding.all(10),
                    bgcolor=ft.Colors.GREY_100
                )
            ]
        )

        # --- Conexión de Eventos de Escaneo ---
        # Conexión del botón de escaneo principal (usa la IP WAN predeterminada)
        self.scan_button.on_click = lambda e: self.scanner.scan_ports(
            page=page,
            results_column=self.results_column,
            loading_row=self.loading_row,
            scan_button=self.scan_button,
            ip_textfield=self.ip_textfield,
            scan_ip_button=self.scan_ip_button
        )
        
        # Conexión del botón de escaneo de IP personalizada
        self.scan_ip_button.on_click = lambda e: self.scanner.scan_ports(
            # Pasa la IP ingresada como argumento 'target_ip'
            target_ip=self.ip_textfield.value, 
            page=page,
            results_column=self.results_column,
            loading_row=self.loading_row,
            scan_button=self.scan_button,
            ip_textfield=self.ip_textfield,
            scan_ip_button=self.scan_ip_button
        )

    def _create_header(self):
        """
        Crea y retorna el contenedor que actúa como cabecera o título de la vista.

        :returns: Un objeto ft.Container que contiene el título con icono de router.
        :rtype: ft.Container
        """
        return ft.Container(
            padding=ft.padding.only(bottom=20),
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ROUTER, size=30, color=ft.Colors.AMBER),
                            ft.Text(
                                value="ESCANEO LOCAL",
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