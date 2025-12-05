import flet as ft
import re
from services.api_service import ApiService

def handle_save(self, e):
    """
    Manejador del evento de clic del botón guardar.
    Valida los campos, crea el enlace en la API y lo agrega a la tabla.
        
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
    
    # Validar formato de IP del DVR si se proporciona
    if self.dvr_ip_textfield.value:
        ip_pattern = r"^([0-9]{1,3}\.){3}[0-9]{1,3}$"
        if not re.match(ip_pattern, self.dvr_ip_textfield.value):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("El formato de IP del DVR no es válido (ej: 192.168.1.1)"),
                bgcolor=ft.Colors.RED_400
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Validar que cada octeto esté entre 0-255
        octetos = self.dvr_ip_textfield.value.split(".")
        for octeto in octetos:
            if int(octeto) > 255:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("IP inválida: cada octeto debe estar entre 0-255"),
                    bgcolor=ft.Colors.RED_400
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
    
    # Validar formato de MAC del DVR si se proporciona
    if self.dvr_mac_textfield.value:
        mac_pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
        if not re.match(mac_pattern, self.dvr_mac_textfield.value):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("El formato de MAC del DVR no es válido (ej: 00:1A:2B:3C:4D:5E)"),
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
    
    # Intentar crear el enlace en la API
    print(f"Creando enlace: {enlace_data['nombre']}")
    api_result = ApiService.create_link(enlace_data)
    
    if api_result["success"]:
        print(f"Enlace creado exitosamente: {api_result['message']}")
        
        # Llamar al callback local para agregar a la tabla
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
        
        # Mostrar mensaje de éxito
        try:
            snackbar = ft.SnackBar(
                ft.Text("Enlace creado exitosamente", color=ft.Colors.WHITE),
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
    else:
        # Mostrar error
        print(f"Error al crear enlace: {api_result['message']}")
        try:
            snackbar = ft.SnackBar(
                ft.Text(f"Error: {api_result['message']}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
                duration=5000
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()
        except Exception as ex:
            print(f"Error showing snackbar: {ex}")