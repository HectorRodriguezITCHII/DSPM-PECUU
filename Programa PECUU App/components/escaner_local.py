import urllib.request
import socket
import sys
import flet as ft

class NetworkScanner:
    """
    Clase que gestiona las operaciones de red, incluyendo la obtención de 
    direcciones IP local y pública (WAN), y la funcionalidad de escaneo de puertos.
    
    Los resultados de IP se obtienen al instanciar la clase y se almacenan 
    como atributos.
    """
    def __init__(self, wan_url='https://api.ipify.org'):
        """
        Inicializa la clase, obtiene las direcciones IP y define la lista 
        de puertos por defecto.

        :param wan_url: URL del servicio web utilizado para obtener la IP pública.
        :type wan_url: str
        """
        self.lan_ip = self.get_lan_ip()
        self.wan_ip = self.get_wan_ip(wan_url)
        # Puertos por defecto para el escaneo (comunes en cámaras y servicios web)
        self.default_ports = [80, 81, 82, 554, 1024, 1025]
    
    def get_lan_ip(self):
        """
        Obtiene la dirección IP local (LAN) del host.

        Establece una conexión temporal a una IP no enrutada (10.255.255.255) 
        para forzar al sistema a devolver la IP de la interfaz de red activa.

        :returns: La dirección IP local (LAN) como cadena, o '127.0.0.1' si falla.
        :rtype: str
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Conexión ficticia para obtener la IP de origen
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def get_wan_ip(self, wan_url):
        """
        Obtiene la dirección IP pública (WAN) del host utilizando un servicio 
        web externo (ej. ipify.org).

        :param wan_url: URL del servicio web que retorna la IP pública.
        :type wan_url: str
        :returns: La dirección IP pública (WAN) como cadena, o None si falla.
        :rtype: str or None
        """
        try:
            wan_ip = urllib.request.urlopen(wan_url).read().decode('utf8')
            return wan_ip
        except Exception as e:
            print(f"Error al obtener la IP pública: {e}")
            return None
    
    def scan_ports(self, target_ip=None, port_list=None, page=None, results_column=None, loading_row=None, scan_button=None, ip_textfield=None, scan_ip_button=None):
        """
        Ejecuta un escaneo de puertos TCP en una dirección IP objetivo, 
        actualizando los componentes de la UI de Flet.

        :param target_ip: Dirección IP a escanear. Si es None, usa self.wan_ip.
        :type target_ip: str, opcional
        :param port_list: Lista de puertos a escanear. Si es None, usa self.default_ports.
        :type port_list: list[int], opcional
        :param page: Objeto ft.Page para forzar actualizaciones de la UI.
        :type page: ft.Page, opcional
        :param results_column: ft.Column donde se mostrarán los resultados.
        :type results_column: ft.Column, opcional
        :param loading_row: ft.Row que contiene el indicador de carga y el texto de estado.
        :type loading_row: ft.Row, opcional
        :param scan_button: Botón de escaneo WAN (se deshabilita).
        :type scan_button: ft.FilledButton, opcional
        :param ip_textfield: Campo de texto de entrada de IP (se deshabilita).
        :type ip_textfield: ft.TextField, opcional
        :param scan_ip_button: Botón de escaneo de IP personalizada (se deshabilita).
        :type scan_ip_button: ft.IconButton, opcional
        """
        # --- 1. Deshabilitar Controles de UI ---
        scan_button.disabled = True 
        scan_button.bgcolor = ft.Colors.GREY_500
        scan_button.color = ft.Colors.GREY_600

        scan_ip_button.disabled = True
        scan_ip_button.bgcolor = ft.Colors.GREY_500
        scan_ip_button.icon_color = ft.Colors.GREY_600

        ip_textfield.disabled = True
        ip_textfield.bgcolor = ft.Colors.GREY_300
        ip_textfield.color = ft.Colors.GREY_400

        if page and hasattr(page, "update"):
            page.update()

        if results_column is not None:
            results_column.controls.clear()

        # --- 2. Configuración y Visibilidad del Indicador de Carga ---
        loading_indicator = None
        status_text = None
        if loading_row is not None and hasattr(loading_row, "controls") and len(loading_row.controls) >= 2:
            loading_indicator = loading_row.controls[0]
            status_text = loading_row.controls[1]

        loading_row.visible = True
        loading_indicator.visible = True
        status_text.value = "Escaneando puertos..."
        status_text.color = ft.Colors.BLACK
        status_text.visible = True
        page.update()

        # --- 3. Determinación de IP y Lista de Puertos ---
        if target_ip is None:
            target_ip = self.wan_ip
        
        if port_list is None:
            port_list = self.default_ports
        
        # --- 4. Bucle de Escaneo de Puertos ---
        for port in port_list:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                status = sock.connect_ex((target_ip, port))
                
                if status == 0:
                    if results_column is not None:
                        results_column.controls.append(
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"Puerto {port}:", color=ft.Colors.GREY_700, size=18),
                                    ft.Text("ABIERTO", color=ft.Colors.GREEN, size=18, weight=ft.FontWeight.BOLD)
                                ]
                            )
                        )
                else:
                    if results_column is not None:
                        results_column.controls.append(
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"Puerto {port}:", color=ft.Colors.GREY_700, size=18),
                                    ft.Text("CERRADO", color=ft.Colors.RED, size=18, weight=ft.FontWeight.BOLD)
                                ]
                            )
                        )

                sock.close()
            except socket.error as err:
                # Manejo de errores de conexión (ej. host inalcanzable, fallo de red)
                if results_column is not None:
                    err_row = ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ERROR, color=ft.Colors.ORANGE),
                            ft.Text(f"Puerto {port}: ERROR DE CONEXIÓN", color=ft.Colors.ORANGE, size=18)
                        ]
                    )
                    results_column.controls.append(err_row)
                sock.close()

        # --- 5. Habilitación Final de Controles de UI ---
        if scan_button is not None:
            scan_button.disabled = False
            scan_button.bgcolor = ft.Colors.INDIGO_700
            scan_button.color = ft.Colors.WHITE
            
        if loading_row is not None:
            loading_row.visible = False
            
        if ip_textfield is not None:
            ip_textfield.disabled = False
            ip_textfield.bgcolor = ft.Colors.WHITE
            ip_textfield.color = ft.Colors.GREY_700
            
        if scan_ip_button is not None:
            scan_ip_button.disabled = False
            scan_ip_button.bgcolor = ft.Colors.INDIGO_500
            scan_ip_button.icon_color = ft.Colors.WHITE
            
        if page and hasattr(page, "update"):
            page.update()

        