import flet as ft
from components.escaner_local import NetworkScanner

class EscanerLocal(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        # Elementos de la barra de carga
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
        
        # Información de red
        self.info_text = ft.Text(
            value="INFORMACIÓN DE LA RED:",
            size=22,
            color=ft.Colors.GREY_700,
            weight="bold"
        )

        # crear instancia del scanner y obtener IPs
        self.scanner = NetworkScanner()

        self.info_lan_text = ft.Text(
            value="IP Local (LAN): " + (self.scanner.lan_ip or ""),
            size=18,
            color=ft.Colors.GREY_700,
        )

        self.info_wan_text = ft.Text(
            value="IP Pública (WAN): " + (self.scanner.wan_ip or ""),
            size=18,
            color=ft.Colors.GREY_700,
        )

        #Contenedor de información de red
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

        # Botón de escaneo
        self.scan_button = ft.FilledButton(
            text="ESCANEAR " + (self.scanner.wan_ip or ""),
            width=300,
            height=50,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=22, weight="bold")),
        )

        # Campo de texto para ingresar IP personalizada
        self.ip_textfield = ft.TextField(
            width=240,
            height=50,
            hint_text="O escanear una IP...",
            text_style=ft.TextStyle(size=16, color=ft.Colors.GREY_700),
            border_color=ft.Colors.GREY_300,
            border_radius=10
        )

        # Botón para escanear IP personalizada
        self.scan_ip_button = ft.IconButton(
            icon=ft.Icons.WIFI_TETHERING,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.INDIGO_500,
            width=50, height=50,
            hover_color=ft.Colors.INDIGO_400
        )

        # Fila para ingresar IP personalizada y escanearla
        self.ingresar_ip_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.ip_textfield,
                self.scan_ip_button
            ]
        )

        #Contenedor con botón y fila de ingreso de IP
        self.buttons_container = ft.Container(
            margin=ft.margin.only(bottom=20),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.scan_button, self.ingresar_ip_row]
            )
        )

        # Fila de carga y estado
        self.loading_row = ft.Row(
            controls=[self.loading_indicator, self.status_text],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )

        # Columna para resultados del escaneo
        self.results_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Contenedor principal
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

        # Conectar botón al manejador de escaneo usando kwargs para evitar reordenamiento accidental
        self.scan_button.on_click = lambda e: self.scanner.scan_ports(
            page=page,
            results_column=self.results_column,
            loading_row=self.loading_row,
            scan_button=self.scan_button,
            ip_textfield=self.ip_textfield,
            scan_ip_button=self.scan_ip_button
        )
    
    def _create_header(self):
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