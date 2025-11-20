import flet as ft

def handle_save(self, e):
    """
    Manejador del evento de clic del botón guardar.
    Valida los campos y agrega un nuevo enlace a la tabla.
        
    :param e: Evento de clic.
    """
    # Validar que los campos obligatorios no estén vacíos
    if not self.name_textfield.value or not self.ddns_textfield.value:
        # Mostrar alerta si faltan campos
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Por favor, completa al menos el Nombre y DDNS"),
            bgcolor=ft.Colors.RED_400
        )
        self.page.snack_bar.open = True
        self.page.update()
        return
        
    # Crear diccionario con los datos del enlace
    enlace_data = {
        "nombre": self.name_textfield.value,
        "ddns": self.ddns_textfield.value,
        "puerto_http": self.http_port_dropdown.value or "80",
        "puerto_rtsp": self.rtsp_port_dropdown.value or "554",
        "wifi_nombre": self.wifi_name_textfield.value or "",
        "wifi_password": self.wifi_password_textfield.value or "",
        "modem_password": self.modem_password_textfield.value or "",
        "dvr_ip": self.dvr_ip_textfield.value or "",
        "dvr_mac": self.dvr_mac_textfield.value or "",
    }
        
    # Llamar al callback para agregar el enlace
    if self.add_enlace_callback:
        self.add_enlace_callback(enlace_data)
        
    # Limpiar los campos
    self.name_textfield.value = ""
    self.ddns_textfield.value = ""
    self.http_port_dropdown.value = None
    self.rtsp_port_dropdown.value = None
    self.wifi_name_textfield.value = ""
    self.wifi_password_textfield.value = ""
    self.modem_password_textfield.value = ""
    self.dvr_ip_textfield.value = ""
    self.dvr_mac_textfield.value = ""
        
    # Mostrar mensaje de éxito con Snackbar
    try:
        snackbar = ft.SnackBar(
            ft.Text("Enlace agregado exitosamente", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700,
            duration=3000
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
    except Exception as ex:
        print(f"Error showing snackbar: {ex}")
        
    # Regresar a la vista de enlaces
    if self.change_view:
        self.change_view("enlaces")