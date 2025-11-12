import flet as ft
import os
from components.header import Header
from components.menu import Menu
from views.actividades import Actividades
from views.escaner_general import EscanerGeneral
from views.escaner_local import EscanerLocal
from views.enlaces import Enlaces
from views.logs import Logs
from views.usuarios import Usuarios

class MainApp(ft.Container):
    """
    Clase principal que define la estructura y el comportamiento de la
    interfaz de usuario de la aplicación.

    Hereda de ft.Container para ocupar toda la página y gestiona el
    Header, el Menú de navegación y las Vistas principales (Escaner).
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa la aplicación principal y configura la página de Flet.

        :param page: El objeto ft.Page proporcionado por el framework Flet.
        :type page: ft.Page
        """
        super().__init__(expand=True)
        self.page = page
        self.page.title = "Sistema de Gestión de Cámaras Ciudadanas"
        self.page.bgcolor = ft.Colors.WHITE
        
        # Componentes de la interfaz
        self.header = Header(page)
        self.menu = Menu(page)
        
        # Vistas dinámicas de la aplicación
        # Las instancias de las vistas son creadas aquí para ser reutilizadas.
        self.views = {
            "actividades": Actividades(page),
            "escaner_general": EscanerGeneral(page),
            "escaner_local": EscanerLocal(page),
            "enlaces": Enlaces(page),
            "historial": Logs(page),
            "usuarios": Usuarios(page),
        }
        
        # Configurar los manejadores de eventos para los botones del menú
        self.setup_menu_events()
        
        # Vista inicial al cargar la aplicación
        self.current_view = self.views["actividades"]
        
        # Cuerpo principal (Contenedor que alberga el Menú y la Vista actual)
        self.body = ft.Container(
            expand=True,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.menu,
                    self.current_view
                ]
            )
        )
        
        # Agregar el diseño final a la página de Flet (Header y Body)
        self.page.add(ft.Column(
            expand=True,
            controls=[
                self.header,
                self.body
            ]
        ))
    
    def setup_menu_events(self):
        """
        Asigna la función 'change_view' a los eventos 'on_click' de los 
        botones del menú (tanto en 'Menu' como en 'Header').
        
        Nota: Se utilizan funciones lambda para pasar el nombre de la vista 
        como argumento.
        """
        # Configurar eventos del menú lateral
        self.menu.actividades_btn.on_click = lambda e: self.change_view("actividades")
        self.menu.escaner_general_btn.on_click = lambda e: self.change_view("escaner_general")
        self.menu.escaner_local_btn.on_click = lambda e: self.change_view("escaner_local")
        self.menu.enlaces_btn.on_click = lambda e: self.change_view("enlaces")
        self.menu.historial_btn.on_click = lambda e: self.change_view("historial")
        self.menu.usuarios_btn.on_click = lambda e: self.change_view("usuarios")

    def change_view(self, view_name):
        """
        Cambia la vista actual en el cuerpo principal de la aplicación.
        
        Si la vista no existe en 'self.views', muestra un mensaje de error.

        :param view_name: Nombre (clave) de la vista a mostrar.
        :type view_name: str
        """
        # Reemplaza el control en el índice 1 del ft.Row (la vista actual)
        # con la nueva vista obtenida del diccionario 'self.views'.
        self.body.content.controls[1] = self.views.get(
            view_name, ft.Text("Vista no disponible")
        )

        # Actualizar el estado visual (ícono/color) del menú
        try:
            self.menu.set_selected(view_name)
        except Exception:
            # Capturar excepciones si el nombre de la vista no corresponde
            # a un botón en el menú (ej. vista de "usuarios" o "actividades")
            pass
        
        # Forzar la actualización de la interfaz de usuario de Flet
        self.page.update()

def main(page: ft.Page):
    """
    Función principal de Flet que se ejecuta al iniciar la aplicación.
    
    Configura la ruta de los assets y lanza la instancia de MainApp.

    :param page: El objeto ft.Page proporcionado por Flet.
    :type page: ft.Page
    """
    # Obtener la ruta absoluta del directorio donde se ejecuta el script (main.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta al directorio de assets (src/assets)
    assets_path = os.path.join(base_dir, "src", "assets")
    page.assets_dir = assets_path
    
    # Inicializar y correr la aplicación principal
    MainApp(page)

if __name__ == "__main__":
    """
    Punto de entrada del script.
    
    Inicia la aplicación de Flet con la función 'main' como destino.
    """
    # Ejecutar la app de Flet
    ft.app(target=main)