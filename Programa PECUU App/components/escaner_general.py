import socket
import flet as ft
import time
from services.api_service import ApiService

PORT_LIST = [80, 81, 82, 83, 84, 85, 86, 87, 88, 554, 1024, 1025, 1026, 1027, 1028, 1029]

# Las URLs ahora se cargan dinámicamente desde la API
# Este es un fallback en caso de que la API falle
PREDEFINED_URLS = []

def scan_ports(ip_addr: str, results_column: ft.Column):
    """
    Intenta establecer una conexión TCP con una dirección IP en la lista de puertos predefinidos.

    Utiliza un socket con un tiempo de espera de 3 segundos para determinar 
    si el puerto está abierto o cerrado.

    :param ip_addr: Dirección IP (v4) a escanear.
    :type ip_addr: str
    :param results_column: Columna de Flet donde se podría mostrar un mensaje de error 
                           de conexión (no de puerto cerrado).
    :type results_column: ft.Column
    :returns: Una tupla que contiene dos listas: puertos abiertos y puertos cerrados.
    :rtype: tuple[list[int], list[int]]
    """
    open_ports = []
    closed_ports = []
    
    for port in PORT_LIST:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            status = sock.connect_ex((ip_addr, port))
            
            if status == 0:
                open_ports.append(port)
            else:
                closed_ports.append(port)
            sock.close()
            
        except socket.error as err:
            results_column.controls.append(
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.ORANGE),
                ft.Text(f"Puerto {port}: ERROR DE CONEXIÓN", color=ft.Colors.ORANGE, size=16)
            )
            continue
        
    return open_ports, closed_ports


def scan_urls_handler(e, results_column: ft.Column, loading_row: ft.Row, scan_button: ft.FilledButton, page: ft.Page):
    """
    Manejador de eventos para iniciar el Escaneo General de DDNS desde la API.

    Obtiene la lista de DDNS de la API y escanea solo esos enlaces.
    Gestiona la UI (deshabilitación/habilitación del botón, visibilidad de carga) 
    y la lógica de escaneo.

    :param e: Objeto de evento de Flet (el evento de clic del botón).
    :param results_column: Columna de Flet donde se mostrarán los resultados finales.
    :type results_column: ft.Column
    :param loading_row: Fila de Flet que contiene el indicador de carga y el texto de estado.
    :type loading_row: ft.Row
    :param scan_button: El botón de escaneo para ser deshabilitado durante el proceso.
    :type scan_button: ft.FilledButton
    :param page: La página principal de Flet, utilizada para forzar las actualizaciones de UI.
    :type page: ft.Page
    """
    # --- Configuración Inicial de UI ---
    scan_button.disabled = True
    scan_button.bgcolor = ft.Colors.GREY_500
    scan_button.color = ft.Colors.GREY_600
    page.update()
    
    results_column.controls.clear()

    loading_indicator = loading_row.controls[0]
    status_text = loading_row.controls[1]

    loading_row.visible = True
    loading_indicator.visible = True
    status_text.value = "Cargando enlaces de la API..."
    status_text.color = ft.Colors.BLACK
    status_text.visible = True
    page.update()

    # Obtener URLs/DDNS desde la API
    print("[INFO] Obteniendo enlaces desde la API...")
    enlaces = ApiService.get_links()
    
    if not enlaces:
        results_column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(name=ft.Icons.ERROR, size=50, color=ft.Colors.RED_700),
                    ft.Text("No se pudieron obtener los enlaces desde la API", 
                           weight="bold", color=ft.Colors.RED_700, size=14),
                    ft.Text("Verifica tu conexión a internet", 
                           color=ft.Colors.RED_600, size=12)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                margin=10,
                bgcolor=ft.Colors.RED_50,
                border_radius=10,
                width=500
            )
        )
        loading_row.visible = False
        scan_button.disabled = False
        scan_button.bgcolor = ft.Colors.INDIGO_700
        scan_button.color = ft.Colors.WHITE
        page.update()
        return
    
    # Extraer solo los DDNS
    urls = [enlace.get("ddns", "") for enlace in enlaces if enlace.get("ddns")]
    urls = [url for url in urls if url]  # Filtrar vacíos
    
    print(f"[INFO] Se obtuvieron {len(urls)} DDNS para escanear")
    print(f"[DEBUG] DDNS: {urls}")

    if not urls:
        results_column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("No hay DDNS configurados en la API para escanear", 
                           weight="bold", color=ft.Colors.ORANGE_700, size=14),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                margin=10,
                bgcolor=ft.Colors.ORANGE_50,
                border_radius=10,
                width=500
            )
        )
        loading_row.visible = False
        scan_button.disabled = False
        scan_button.bgcolor = ft.Colors.INDIGO_700
        scan_button.color = ft.Colors.WHITE
        page.update()
        return

    # Lista para almacenar los resultados del escaneo
    scan_results = []
    total_scanned = 0
    
    status_text.value = "Escaneando DDNS..."
    page.update()
    
    # Escanear cada DDNS
    for url in urls:
        try:
            ip_addr = socket.gethostbyname(url)
            open_ports, closed_ports = scan_ports(ip_addr, results_column)
            total_scanned += 1
            
            scan_results.append({
                'url': url,
                'ip': ip_addr,
                'open_ports': open_ports,
                'closed_ports': closed_ports,
                'status': 'success'
            })
            
            # Actualizar el contador durante el escaneo
            status_text.value = f"Escaneando... {total_scanned}/{len(urls)}"
            page.update()

        except socket.gaierror:
            total_scanned += 1
            # Error al resolver DNS
            scan_results.append({
                'url': url,
                'ip': 'No se pudo resolver',
                'open_ports': [],
                'closed_ports': [],
                'status': 'dns_error',
                'error': 'Error al resolver DNS'
            })
            status_text.value = f"Escaneando... {total_scanned}/{len(urls)}"
            page.update()
            continue
        except Exception as ex:
            total_scanned += 1
            scan_results.append({
                'url': url,
                'ip': 'Error',
                'open_ports': [],
                'closed_ports': [],
                'status': 'error',
                'error': str(ex)
            })
            status_text.value = f"Escaneando... {total_scanned}/{len(urls)}"
            page.update()
            continue

    # Limpiar los resultados anteriores
    results_column.controls.clear()
    
    # Mostrar encabezado con estadísticas
    results_column.controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text("RESULTADOS DEL ESCANEO DE DDNS", 
                       size=20, weight="bold", color=ft.Colors.BLUE_800),
                ft.Text(f"Total de DDNS escaneados: {total_scanned}", 
                       size=16, weight="bold", color=ft.Colors.GREY_600),
                ft.Divider(height=2, color=ft.Colors.GREY_400)
            ]),
            padding=15,
            margin=5,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            width=500
        )
    )
    
    # Mostrar resultados detallados
    if scan_results:
        for item in scan_results:
            if item['status'] == 'success':
                # DDNS escaneado exitosamente
                container_content = [
                    ft.Row([
                        ft.Icon(name=ft.Icons.PERM_SCAN_WIFI, 
                               color=ft.Colors.GREEN_400 if item['open_ports'] else ft.Colors.RED_400),
                        ft.Text(f"{item['url']}", weight="bold", size=14, color=ft.Colors.GREY_800)
                    ]),
                    ft.Text(f"IP: {item['ip']}", size=12, color=ft.Colors.GREY_500),
                    ft.Text(f"Puertos abiertos: {', '.join(map(str, item['open_ports'])) if item['open_ports'] else 'Ninguno'}", 
                           weight="bold", 
                           color=ft.Colors.GREEN_600 if item['open_ports'] else ft.Colors.GREY_600,
                           size=12),
                    ft.Text(f"Puertos cerrados: {', '.join(map(str, item['closed_ports'])) if item['closed_ports'] else 'N/A'}", 
                           size=12, color=ft.Colors.GREY_600),
                ]
                bg_color = ft.Colors.GREEN_50 if item['open_ports'] else ft.Colors.GREY_100
                border_color = ft.Colors.GREEN_200 if item['open_ports'] else ft.Colors.GREY_200
                
            else:
                # Error en el DDNS
                container_content = [
                    ft.Row([
                        ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.RED_400),
                        ft.Text(f"{item['url']}", weight="bold", size=14, color=ft.Colors.GREY_800)
                    ]),
                    ft.Text(f"Estado: {item['error']}", color=ft.Colors.RED_600, size=12)
                ]
                bg_color = ft.Colors.RED_50
                border_color = ft.Colors.RED_200

            results_column.controls.append(ft.Container(
                content=ft.Column(container_content),
                padding=12,
                margin=3,
                bgcolor=bg_color,
                border=ft.border.all(1, border_color),
                border_radius=8,
                width=500
            ))

    loading_row.visible = False

    # Mensaje final
    results_column.controls.append(
        ft.Row(
            [
                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_700),
                ft.Text("Escaneo completado.", weight="bold", color=ft.Colors.GREEN_700, size=18)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    scan_button.disabled = False
    scan_button.bgcolor = ft.Colors.INDIGO_700
    scan_button.color = ft.Colors.WHITE
    page.update()