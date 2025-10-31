import socket
import flet as ft
import time

PORT_LIST = [80, 81, 82, 83, 554, 1024, 1025, 1026]

PREDEFINED_URLS = [
    "fracmontevesubio.zona2.ddnsgroup.com", "contructoramarro.zona2.ddnsgroup.com",
    "plazagalerias3.ddnsgroup3.com", "bodegacmarro.ddnsgroup.com",
    "ductosyrecinas.ddnsgroup.com", "201.174.26.114",
    "daserblinds.zona2.ddnsgroup.com", "cabus.zona2.ddnsgroup.com",
    "chih.tannermh.net", "pomega.net", "fmradiocom.ddnsgroup3.com",
    "lensdepot.zona2.ddnsgroup.com", "nahol.zona2.ddnsgroup.com",
    "ferreteriacamachisa.ddnsgroup.com", "americansourse.zona2.ddnsgroup.com",
    "sec6.zona2.ddnsgroup.com", "201.174.173.132",
    "estatal3015.ddnsgroup3.com", "ysletagarage.zona2.ddnsgroup.com",
    "newberry.ddnsgroup.com", "haciendassantafe.ddnsgroup3.com",
    "grvisassanfelipe.ddnsgroup3.com", "grvisasnorte.ddnsgroup.com",
    "148.229.4.10", "201.144.106.115", "suitesoficinas.xnet.mx",
    "vistas.xnet.mx", "expressoficinas.xnet.mx", "sanjose.ddnsgroup3.com",
    "famcarrasco.zona2.ddnsgroup.com", "ccleaner.zona2.ddnsgroup.com",
    "desponchado7.zona2.ddnsgroup.com", "famdelvillar.ddnsgroup.com",
    "modelorama80.zona2.ddnsgroup.com", "cerradaparis.ddnsgroup.com",
    "grupotulpe2.ddnsgroup3.com", "pilargarciagonzalez.ddnsgroup3.com",
    "expendiodecarne.zona2.ddnsgroup.com", "quintasdelsolsosa.ddnsgroup.com",
    "201.100.18.16", "clinicacumbres.ddnsgroup.com",
    "rinconfloral.ddnsgroup3.com", "fraccmolino.zona2.ddnsgroup.com",
    "172.20.2.123", "10.218.221.60", "grupoikvi.ddnsgroup3.com",
    "cmic.fortiddns.com", "cromadora.ddnsgroup.com",
    "expendiodeleche.ddnsgroup.com", "maquinado.zona2.ddnsgroup.com",
    "seminuevoslisboa.zona2.ddnsgroup.com", "juanacata.zona2.ddnsgroup.com",
    "estancia2708.ddnsgroup.com", "vpn2expo.ddns.net",
    "hiperplaza.ddnsgroup.com", "10.218.56.33",
    "bosquesdelvalle1.ddnsgroup3.com", "hogarangelica.zona2.ddnsgroup.com",
    "rojacell.ddnsgroup.com", "esteticadelucero.ddnsgroup.com",
    "comercializadoraautomotriz.zona2.ddnsgroup.com", "barqueta.ddnsgroup.com",
    "abastos.ddnsgroup.com", "famsifuentes.ddnsgroup.com",
    "mayoreodelascolchas.zona2.ddnsgroup.com", "pinturasalfagama.zona2.ddnsgroup.com",
    "alfagama.ddns.net", "cafeteca.ddnsgroup3.com",
    "caritasmorelos.ddnsgroup.com", "10.218.247.30",
    "catarrocedis.ddnsgroup3.com", "sorianalasierra.ddnsgroup3.com",
    "subwayadelita.ddnsgroup3.com", "opus21boutique.ddnsgroup3.com",
    "primagustinmelgarsur.ddnsgroup3.com", "licorerialamorita.ddnsgroup3.com",
    "notaria24.ddnsgroup3.com", "raibu.ddnsgroup3.com",
    "petro7ferrari.ddnsgroup3.com", "parroquiajuanpablo2.ddnsgroup2.com",
    "gymalfayomega.ddnsgroup3.com", "primariadivisiondelnorte.ddnsgroup2.com",
    "laneurona.ddnsgroup2.com", "petro7maya.ddnsgroup2.com",
    "petro7cima.ddnsgroup2.com", "petro7lisboa.ddnsgroup3.com",
    "petro7kop.ddnsgroup2.com", "bachilleratoaltavista.ddnsgroup3.com",
    "escjosemariamorelos.ddnsgroup3.com", "cedinorte.ddnsgroup2.com",
    "famecheverria.ddnsgroup2.com", "sanjoseenlamontana.ddnsgroup2.com",
    "189.206.221.182", "148.244.109.189", "casacultura.ddnsgroup2.com",
    "189.206.69.69", "201.132.82.131", "45.174.77.102",
    "200.94.16.149", "201.151.94.205", "187.190.255.22",
    "fammatasolis.ddnsgroup2.com", "calle23509.ddnsgroup2.com",
    "calle31901.ddnsgroup2.com", "gloriavilla.ddnsgroup2.com", 
    "evelingonzalez.ddnsgroup2.com", "modelorama285.ddnsgroup2.com",
    "memoherrera.ddnsgroup3.com", "margaritamazadejuarez.ddnsgroup2.com",
    "primadolfolopezmateos.ddnsgroup2.com", "carlosparra.ddnsgroup2.com",
    "drvacacortes.ddnsgroup3.com", "kinderebani.ddnsgroup2.com",
    "edificioroka.ddnsgroup3.com", "loshuertos3.ddnsgroup2.com",
    "rousseau.ddnsgroup2.com", "secfed1.ddnsgroup3.com",
    "vecjuntarios1.ddnsgroup3.com", "diazdavid.ddnsgroup3.com",
    "carlamariaherrera.ddnsgroup3.com", "casetalomas.ddnsgroup2.com",
    "plazafiesta.ddnsgroup3.com", "escpablogomezrmz.ddnsgroup3.com",
    "notaria19.ddnsgroup3.com", "hinocamiones.ddnsgroup2.com",
    "iglesiaodrenuevo.ddnsgroup3.com", "semillaslagranjita.ddnsgroup3.com",
    "secundaria3013.ddnsgroup3.com", "cam23.ddnsgroup3.com",
    "magpegarciavillalobos.ddnsgroup3.com", "escvictorhugorasconbanda.ddnsgroup3.com",
    "maestrosmexicanos.ddnsgroup.com", "famguerra.ddnsgroup3.com",
    "187.102.204.131", "cam7009.ddnsgroup3.com",
    "rinconadasdelvalle3.ddnsgroup3.com", "escuelaseccion42.ddnsgroup3.com",
    "colegiosathya.ddnsgroup3.com", "prim24feb.ddnsgroup3.com",
    "industriaforestal.ddnsgroup3.com", "kindertarike.ddnsgroup3.com",
    "primchihuahua.ddnsgroup3.com", "falianzacentro.ddnsgroup3.com",
    "falianzafcovilla.ddnsgroup3.com", "ecoplomer.ddnsgroup3.com",
    "148.229.10.240", "falianzaortopedicos.ddnsgroup3.com",
    "148.244.112.140", "primsalvadorallende.ddnsgroup3.com",
    "secfed9.ddnsgroup3.com", "magdarivera.ddnsgroup3.com",
    "cumbrespedregal.ddnsgroup3.com", "nuevochihuahua.ddnsgroup3.com",
    "primveteranos.ddnsgroup3.com", "sectec3060.ddnsgroup3.com",
    "rociomendoza.ddnsgroup3.com", "201.174.104.10",
    "201.174.123.235", "virginiachacon.ddnsgroup3.com",
    "ambar.ddnsgroup3.com", "primrevmex.ddnsgroup3.com",
    "zaakborjas.ddnsgroup3.com", "adrianpavia.ddnsgroup3.com",
    "lomasdelvalle.ddnsgroup3.com", "altozanochh.camdvr.org",
    "bodeguitaocampo.ddnsgroup3.com", "bodeguitaninosheroes.ddnsgroup3.com",
    "alejandrotavares.ddnsgroup3.com", "secfed10.ddnsgroup3.com",
    "10.218.64.81", "primagustinmelgar.ddnsgroup3.com",
    "bodeguitaarboledas.ddnsgroup3.com", "bodeguitasanfelipe.ddnsgroup3.com",
    "fabiolacorral.ddnsgroup3.com", "patriciarodriguez.ddnsgroup3.com",
    "tecnica99.ddnsgroup3.com", "10.218.81.3",
    "oxxogascamionero2.ddnsgroup3.com", "danielrodriguez.ddnsgroup3.com",
    "primponcedeleon.ddnsgroup3.com", "yoloxochitltorres.ddnsgroup3.com",
    "tinystockjuanescutia.ddnsgroup3.com", "minisuperarana.ddnsgroup3.com",
    "cruzrojacentro.ddnsgroup3.com", "kinderfcomarquez.ddnsgroup3.com",
    "10.218.130.234", "fracctica.ddnsgroup3.com",
    "sec3049.ddnsgroup3.com", "primceciliopolanco.ddnsgroup3.com",
    "oxxogascamionero1.ddnsgroup3.com", "oxxogaspanamericana.ddnsgroup3.com",
    "oxxogasmajalca.ddnsgroup3.com", "fracctaibilla.ddnsgroup3.com",
    "kinderjosevasconcelos.ddnsgroup3.com", "kinderaureliaaguero.ddnsgroup3.com",
    "cediia.ddnsgroup3.com", "nicolasgonzalez.ddnsgroup3.com",
    "fraccvistasdelaslomas.ddnsgroup3.com", "primsalvadorallendetm.ddnsgroup3.com",
    "primadolfolopezmateos.ddnsgroup3.com", "trocesa.ddnsgroup3.com",
    "mistercell.ddnsgroup3.com", "primrotaria7.ddnsgroup2.com",
    "kinderpestalozzi.ddnsgroup2.com", "restauranteayayay.ddnsgroup2.com",
    "10.218.9.112", "148.229.177.243", "primvaletingomezfarias.ddnsgroup3.com",
    "driveinnlahacienda.ddnsgroup.com", "abarrotes34.ddnsgroup.com"
]

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
    # ... (lógica de escaneo con socket)
    return open_ports, closed_ports


def scan_urls_handler(e, results_column: ft.Column, loading_row: ft.Row, scan_button: ft.FilledButton, page: ft.Page):
    """
    Manejador de eventos para iniciar el Escaneo General de todas las URLs predefinidas.

    Gestiona la UI (deshabilitación/habilitación del botón, visibilidad de carga) 
    y la lógica de escaneo. El objetivo principal es encontrar URLs SIN puertos abiertos.

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
    scan_button.disabled = True #Deshabilita el botón al darle click y le da color
    scan_button.bgcolor = ft.Colors.GREY_500
    scan_button.color = ft.Colors.GREY_600
    page.update()
    
    results_column.controls.clear()

    loading_indicator = loading_row.controls[0]
    status_text = loading_row.controls[1]

    loading_row.visible = True
    loading_indicator.visible = True
    status_text.value = "Escaneando..."
    status_text.color = ft.Colors.BLACK
    status_text.visible = True
    page.update()

    urls = PREDEFINED_URLS

    if not urls:
        results_column.controls.append(ft.Text("No hay URLs configuradas para escanear.", color="orange"))
        loading_row.visible = False
        status_text.value = ""
        page.update()
        return

    # Lista para almacenar las URLs sin puertos abiertos
    urls_without_open_ports = []
    total_scanned = 0
    
    # Primero escaneamos todas las URLs
    for url in urls:
        try:
            ip_addr = socket.gethostbyname(url)
            open_ports, closed_ports = scan_ports(ip_addr, results_column)
            total_scanned += 1
            
            # Solo agregamos las URLs que NO tienen puertos abiertos
            if not open_ports:  # Si la lista de puertos abiertos está vacía
                urls_without_open_ports.append({
                    'url': url,
                    'ip': ip_addr,
                    'closed_ports': closed_ports
                })
            
            # Actualizar el contador durante el escaneo
            status_text.value = f"Escaneando... {total_scanned}/{len(urls)}"
            page.update()

        except socket.gaierror:
            total_scanned += 1
            # También incluimos URLs que no se pueden resolver (sin puertos abiertos)
            urls_without_open_ports.append({
                'url': url,
                'ip': 'No se pudo resolver',
                'closed_ports': [],
                'error': 'Error al resolver DNS'
            })
            continue
        except Exception as ex:
            total_scanned += 1
            continue

    # Limpiar los resultados anteriores
    results_column.controls.clear()
    
    # Mostrar encabezado con estadísticas
    results_column.controls.append(
        ft.Container(
            content=ft.Column([
                ft.Text("RESULTADOS DEL ESCANEO", 
                       size=20, weight="bold", color=ft.Colors.BLUE_800),
                ft.Text(f"URLs sin puertos abiertos: {len(urls_without_open_ports)}/{total_scanned}", 
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
    
    # Mostrar solo las URLs sin puertos abiertos
    if urls_without_open_ports:
        for item in urls_without_open_ports:
            # Color de fondo diferente si hay error de DNS
            bg_color = ft.Colors.RED_50 if 'error' in item else ft.Colors.GREY_100
            border_color = ft.Colors.RED_200 if 'error' in item else ft.Colors.GREY_200
            
            container_content = [
                ft.Row([
                ft.Icon(name=ft.Icons.PERM_SCAN_WIFI, color=ft.Colors.RED_400),
                ft.Text(f"{item['url']}", weight="bold", size=14, color=ft.Colors.GREY_800)
                ]),
                ft.Text(f"IP: {item['ip']}", size=12, color=ft.Colors.GREY_500),
            ]
            
            if 'error' in item:
                container_content.append(
                    ft.Text(f"⚠️ {item['error']}", color=ft.Colors.RED_600, size=12)
                )
            else:
                container_content.extend([
                    ft.Text("Puertos abiertos: Ninguno", color=ft.Colors.RED_400, weight="bold"),
                    ft.Text(f"Puertos cerrados: {' '.join(map(str, item['closed_ports'])) if item['closed_ports'] else 'Ninguno'}", 
                           size=12, color=ft.Colors.GREY_600),
                ])

            results_column.controls.append(ft.Container(
                content=ft.Column(container_content),
                padding=12,
                margin=3,
                bgcolor=bg_color,
                border=ft.border.all(1, border_color),
                border_radius=8,
                width=500
            ))
    else:
        results_column.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("🚫 No se encontraron URLs sin puertos abiertos", 
                           weight="bold", color=ft.Colors.ORANGE_700),
                    ft.Text("Todas las URLs escaneadas tienen al menos un puerto abierto.", 
                           color=ft.Colors.ORANGE_600)
                ]),
                padding=15,
                margin=5,
                bgcolor=ft.Colors.ORANGE_50,
                border_radius=10,
                width=500
            )
        )

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