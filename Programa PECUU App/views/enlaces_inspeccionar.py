import flet as ft
from components.inner_header import InnerHeader
from components.enlaces import EnlacesManager

class EnlacesInspeccionar(ft.Container):
    """
    Representa la vista de "Enlaces - Inspeccionar" de la aplicación.

    Hereda de ft.Container y se configura para ocupar toda el área de contenido
    principal de la aplicación. Muestra los detalles de un enlace específico.
    """
    def __init__(self, page: ft.Page, change_view=None, enlace_data=None):
        """
        Inicializa la vista y configura todos los componentes de la interfaz.

        :param page: Objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        :param change_view: Función callback para cambiar de vista.
        :type change_view: callable
        :param enlace_data: Diccionario con los datos del enlace a inspeccionar.
        :type enlace_data: dict
        """
        super().__init__()
        self.page = page
        self.change_view = change_view
        self.enlace_data = enlace_data or {}
        
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
            value=self.enlace_data.get("nombre", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.ddns_textfield = ft.TextField(
            label="URL del Enlace",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("ddns", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.http_port_textfield = ft.TextField(
            label="Puerto HTTP",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("puerto_http", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.rtsp_port_textfield = ft.TextField(
            label="Puerto RTSP",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("puerto_rtsp", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.wifi_name_textfield = ft.TextField(
            label="Nombre de la Red WiFi",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("wifi_nombre", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.wifi_password_textfield = ft.TextField(
            label="Contraseña de la Red WiFi",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("wifi_password", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.modem_password_textfield = ft.TextField(
            label="Contraseña del Modem",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("modem_password", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.dvr_ip_textfield = ft.TextField(
            label="IP del DVR",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("dvr_ip", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.dvr_mac_textfield = ft.TextField(
            label="MAC del DVR",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("dvr_mac", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.user1_textfield = ft.TextField(
            label="Usuario 1 (Admin)",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("user1", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.user1_password_textfield = ft.TextField(
            label="Contraseña 1 (Admin)",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("user1_password", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.user2_textfield = ft.TextField(
            label="Usuario 2 (DSPM)",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("user2", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        self.user2_password_textfield = ft.TextField(
            label="Contraseña 2 (DSPM)",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
            value=self.enlace_data.get("user2_password", ""),
            disabled=True,
            color=ft.Colors.GREY_700
        )

        # store inner header so we can update its title on save
        self.inner_header = InnerHeader(f"{self.enlace_data.get('nombre', 'ENLACE')}", icon=ft.Icons.VISIBILITY)

        self.edit_button = ft.FilledButton(
            text="EDITAR",
            width=200,
            height=50,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight="bold")),
            on_click=lambda e: self._toggle_edit(e)
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
                self.inner_header,
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    width=700,
                    controls=[
                        ft.Container(
                            padding=ft.padding.all(15),
                            width=700,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.START,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Nombre:", style=ft.TextStyle(size=16)),
                                            self.name_textfield
                                        ]
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.GREY_100,
                            padding=ft.padding.all(15),
                            width=700,
                            border_radius=5,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.START,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("RED:", style=ft.TextStyle(size=20, weight="bold", color=ft.Colors.INDIGO_600)),
                                    ft.Divider(thickness=1, color=ft.Colors.GREY_300),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("SSID:", style=ft.TextStyle(size=16)),
                                            self.wifi_name_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Contraseña:", style=ft.TextStyle(size=16)),
                                            self.wifi_password_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Contraseña del Modem:", style=ft.TextStyle(size=16)),
                                            self.modem_password_textfield
                                        ]
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.GREY_100,
                            padding=ft.padding.all(15),
                            width=700,
                            border_radius=5,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.START,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("DVR:", style=ft.TextStyle(size=20, weight="bold", color=ft.Colors.INDIGO_600)),
                                    ft.Divider(thickness=1, color=ft.Colors.GREY_300),
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
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Usuario 1 (Admin):", style=ft.TextStyle(size=16)),
                                            self.user1_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Contraseña 1 (Admin)", style=ft.TextStyle(size=16)),
                                            self.user1_password_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Usuario 2 (DSPM):", style=ft.TextStyle(size=16)),
                                            self.user2_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Contraseña 2 (DSPM):", style=ft.TextStyle(size=16)),
                                            self.user2_password_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Puerto HTTP:", style=ft.TextStyle(size=16)),
                                            self.http_port_textfield
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Puerto RTSP:", style=ft.TextStyle(size=16)),
                                            self.rtsp_port_textfield
                                        ]
                                    ),   
                                ]
                            ),
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.GREY_100,
                            padding=ft.padding.all(15),
                            width=700,
                            border_radius=5,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.START,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("PECUU:", style=ft.TextStyle(size=20, weight="bold", color=ft.Colors.INDIGO_600)),
                                    ft.Divider(thickness=1, color=ft.Colors.GREY_300),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("DDNS:", style=ft.TextStyle(size=16)),
                                            self.ddns_textfield
                                        ]
                                    ),
                                ]
                            )
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                self.edit_button,
                                self.cancel_button
                            ]
                        )
                    ]
                )
            ]
        )

    def _toggle_edit(self, e):
        editing = getattr(self, '_editing', False)
        if not editing:
            # enable editing
            self._editing = True
            self.edit_button.text = "GUARDAR"
            for fld in [
                self.name_textfield, self.ddns_textfield, self.http_port_textfield,
                self.rtsp_port_textfield, self.wifi_name_textfield, self.wifi_password_textfield,
                self.modem_password_textfield, self.dvr_ip_textfield, self.dvr_mac_textfield,
                self.user1_textfield, self.user1_password_textfield, self.user2_textfield, self.user2_password_textfield
            ]:
                fld.disabled = False
            try:
                self.page.update()
            except Exception:
                pass
        else:
            # save
            self._editing = False
            self.edit_button.text = "EDITAR"
            new_data = {
                'nombre': self.name_textfield.value,
                'ddns': self.ddns_textfield.value,
                'puerto_http': self.http_port_textfield.value,
                'puerto_rtsp': self.rtsp_port_textfield.value,
                'wifi_nombre': self.wifi_name_textfield.value,
                'wifi_password': self.wifi_password_textfield.value,
                'modem_password': self.modem_password_textfield.value,
                'dvr_ip': self.dvr_ip_textfield.value,
                'dvr_mac': self.dvr_mac_textfield.value,
                'user1': self.user1_textfield.value,
                'user1_password': self.user1_password_textfield.value,
                'user2': self.user2_textfield.value,
                'user2_password': self.user2_password_textfield.value,
            }
            original_name = self.enlace_data.get('nombre')
            source = getattr(self, '_source_view', None)
            if source:
                EnlacesManager.update_enlace(source, original_name, new_data)
                # Try to sync our local enlace_data with the attached row data if present
                try:
                    for row in getattr(source, 'data_table', []).rows:
                        if hasattr(row, '_enlace_data') and row._enlace_data.get('nombre') == new_data.get('nombre'):
                            self.enlace_data = row._enlace_data
                            break
                except Exception:
                    # fallback: update local dict
                    try:
                        if isinstance(self.enlace_data, dict):
                            self.enlace_data.update(new_data)
                    except Exception:
                        pass
                # update inner header immediately
                try:
                    if hasattr(self, 'inner_header') and getattr(self.inner_header, 'title_text', None):
                        self.inner_header.title_text.value = self.enlace_data.get('nombre', new_data.get('nombre'))
                        try:
                            self.inner_header.update()
                        except Exception:
                            pass
                except Exception:
                    pass
            for fld in [
                self.name_textfield, self.ddns_textfield, self.http_port_textfield,
                self.rtsp_port_textfield, self.wifi_name_textfield, self.wifi_password_textfield,
                self.modem_password_textfield, self.dvr_ip_textfield, self.dvr_mac_textfield,
                self.user1_textfield, self.user1_password_textfield, self.user2_textfield, self.user2_password_textfield
            ]:
                fld.disabled = True
            # Show snackbar confirming successful save
            try:
                if hasattr(self, 'page') and self.page:
                    snackbar = ft.SnackBar(
                        ft.Text("Enlace guardado exitosamente", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_700,
                        duration=3000
                    )
                    self.page.overlay.append(snackbar)
                    snackbar.open = True
                    self.page.update()
            except Exception as ex:
                print(f"Error showing snackbar: {ex}")
            if self.change_view:
                self.change_view('enlaces')
            else:
                try:
                    self.page.update()
                except Exception:
                    pass
    
