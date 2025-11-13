import flet as ft
from components.inner_header import InnerHeader

class EnlacesAñadir(ft.Container):
    """
    Representa la vista de "Enlaces - Añadir" de la aplicación.

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

        self.name_textfield = ft.TextField(
            label="Nombre del Enlace",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.ddns_textfield = ft.TextField(
            label="URL del Enlace",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.http_port_dropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("80"),
                ft.dropdown.Option("81"),
                ft.dropdown.Option("82"),
            ]
        )

        self.rtsp_port_dropdown = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("554"),
                ft.dropdown.Option("1024"),
                ft.dropdown.Option("1025"),
            ]
        )

        self.wifi_name_textfield = ft.TextField(
            label="Nombre de la Red WiFi",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.wifi_password_textfield = ft.TextField(
            label="Contraseña de la Red WiFi",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.modem_password_textfield = ft.TextField(
            label="Contraseña del Modem",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.dvr_ip_textfield = ft.TextField(
            label="IP del DVR",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.dvr_mac_textfield = ft.TextField(
            label="MAC del DVR",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.save_button = ft.FilledButton(
            text="GUARDAR",
            width=200,
            height=50,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight="bold")),
        )

        self.cancel_button = ft.ElevatedButton(
            text="Regresar",
            width=200,
            height=50,
            color=ft.Colors.INDIGO_500,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18)),
            on_click=lambda e: self.change_view("enlaces") if self.change_view else None
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("AÑADIR ENLACE", icon=ft.Icons.ADD_HOME),
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    width=700,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Nombre:", style=ft.TextStyle(size=16)),
                                self.name_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("DDNS:", style=ft.TextStyle(size=16)),
                                self.ddns_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Puerto HTTP:", style=ft.TextStyle(size=16)),
                                self.http_port_dropdown
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Puerto RTSP:", style=ft.TextStyle(size=16)),
                                self.rtsp_port_dropdown
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Nombre WiFi:", style=ft.TextStyle(size=16)),
                                self.wifi_name_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Contraseña WiFi:", style=ft.TextStyle(size=16)),
                                self.wifi_password_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Contraseña Modem:", style=ft.TextStyle(size=16)),
                                self.modem_password_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("IP del DVR:", style=ft.TextStyle(size=16)),
                                self.dvr_ip_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("MAC del DVR:", style=ft.TextStyle(size=16)),
                                self.dvr_mac_textfield
                            ]
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        self.save_button,
                        self.cancel_button
                    ]
                )
            ]
        )