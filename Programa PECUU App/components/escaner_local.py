import urllib.request
import socket
import sys
import flet as ft

class NetworkScanner:
    def __init__(self, wan_url='https://api.ipify.org'):
        self.lan_ip = self.get_lan_ip()
        self.wan_ip = self.get_wan_ip(wan_url)
        self.default_ports = [80, 81, 82, 554, 1024, 1025]
    
    def get_lan_ip(self):
        """Obtiene la IP local (LAN)"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def get_wan_ip(self, wan_url):
        """Obtiene la IP pública (WAN)"""
        try:
            wan_ip = urllib.request.urlopen(wan_url).read().decode('utf8')
            return wan_ip
        except Exception as e:
            print(f"Error al obtener la IP pública: {e}")
            return None
    
    # Escanea los puertos de una IP específica
    def scan_ports(self, target_ip=None, port_list=None, page=None, results_column=None, loading_row=None, scan_button=None, ip_textfield=None, scan_ip_button=None):
        # Deshabilitar controles durante el escaneo
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

        if target_ip is None:
            target_ip = self.wan_ip
        
        if port_list is None:
            port_list = self.default_ports
        
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
                # Añadir una fila con icono + texto en caso de error
                if results_column is not None:
                    err_row = ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ERROR, color=ft.Colors.ORANGE),
                            ft.Text(f"Puerto {port}: ERROR DE CONEXIÓN", color=ft.Colors.ORANGE, size=18)
                        ]
                    )
                    results_column.controls.append(err_row)
                sock.close()

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

        