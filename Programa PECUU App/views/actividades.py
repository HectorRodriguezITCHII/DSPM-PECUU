import flet as ft
from components.inner_header import InnerHeader
from components.actividades import add_actividad, update_actividad, delete_actividad, toggle_completed_actividad, _update_actividades_container, _create_activity_card
from services.api_service import ApiService

class Actividades(ft.Container):
    """
    Representa la vista de "Actividades" de la aplicación.

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
        self.flet_page = page  # Guardar la referencia a la página de Flet
        self.change_view = change_view
        
        # Lista para almacenar las actividades
        self.actividades = []
        self.actividades_container = ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[]
        )
        
        # Configuración del contenedor principal de la vista
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        self.add_card = ft.Card(
            width=500,
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            ft.Icons.ADD_CIRCLE, 
                            icon_color=ft.Colors.GREY_500, 
                            icon_size=50,
                            on_click=lambda e: self.change_view("actividades_agregar") if self.change_view else None
                        ),
                    ]
                ),
                width=400,
                padding=10,
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
            )
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("ACTIVIDADES", icon=ft.Icons.HOME),
                self.actividades_container
            ]
        )
        
        # Agregar el card de añadir al inicio
        _update_actividades_container(self)
        
        # Cargar actividades desde la API
        self.load_actividades_from_api()
    
    def set_actividades_editar_view(self, actividades_editar_view):
        """
        Establece una referencia a la vista de edición de actividades.
        
        :param actividades_editar_view: Instancia de ActividadesEditar
        """
        self.actividades_editar_view = actividades_editar_view
    
    def add_actividad(self, actividad_data):
        """
        Agrega una nueva actividad a la lista y actualiza la vista.
        
        :param actividad_data: Diccionario con los datos de la actividad
        :type actividad_data: dict
        """
        add_actividad(self, actividad_data)
    
    def update_actividad(self, actividad_index, actividad_data):
        """
        Actualiza una actividad existente en la lista y actualiza la vista.
        
        :param actividad_index: Índice de la actividad a actualizar
        :param actividad_data: Diccionario con los nuevos datos de la actividad
        :type actividad_data: dict
        """
        update_actividad(self, actividad_index, actividad_data)
    
    def delete_actividad(self, actividad_index):
        """
        Elimina una actividad de la lista y actualiza la vista.
        
        :param actividad_index: Índice de la actividad a eliminar
        """
        delete_actividad(self, actividad_index)
    
    def toggle_completed_actividad(self, actividad_index):
        """
        Marca o desmarca una actividad como completada.
        
        :param actividad_index: Índice de la actividad
        """
        toggle_completed_actividad(self, actividad_index)
    
    def _update_actividades_container(self):
        """Actualiza el contenedor de actividades con todas las tarjetas."""
        _update_actividades_container(self)
    
    def _create_activity_card(self, actividad_data):
        """Crea una tarjeta de actividad basada en los datos proporcionados."""
        return _create_activity_card(self, actividad_data)
    
    def load_actividades_from_api(self):
        """
        Carga las actividades desde la API y las muestra en la vista.
        """
        try:
            actividades = ApiService.get_activities()
            if actividades:
                # Limpiar la lista actual
                self.actividades.clear()
                
                # Agregar cada actividad
                for actividad in actividades:
                    self.actividades.append(actividad)
                
                # Actualizar la vista
                _update_actividades_container(self)
                
                print(f"Se cargaron {len(actividades)} actividades desde la API")
            else:
                print("No se pudieron obtener las actividades desde la API")
        except Exception as e:
            print(f"Error al cargar actividades desde la API: {e}")
    
    def refresh_actividades_from_api(self):
        """
        Refresca las actividades desde la API.
        """
        self.load_actividades_from_api()
        if self.flet_page:
            self.flet_page.update()