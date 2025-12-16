import flet as ft
from services.api_service import ApiService

def add_actividad(self, actividad_data):
    """
    Agrega una nueva actividad a la lista y actualiza la vista.
    
    :param actividad_data: Diccionario con los datos de la actividad
    :type actividad_data: dict
    """
    self.actividades.append(actividad_data)
    _update_actividades_container(self)
    self.flet_page.update()

def update_actividad(self, actividad_index, actividad_data):
    """
    Actualiza una actividad existente en la lista y actualiza la vista.
    
    :param actividad_index: Índice de la actividad a actualizar
    :param actividad_data: Diccionario con los nuevos datos de la actividad
    :type actividad_data: dict
    """
    if 0 <= actividad_index < len(self.actividades):
        self.actividades[actividad_index] = actividad_data
        _update_actividades_container(self)
        self.flet_page.update()

def delete_actividad(self, actividad_index):
    """
    Elimina una actividad de la lista y de la API, y actualiza la vista.
    
    :param actividad_index: Índice de la actividad a eliminar
    """
    if 0 <= actividad_index < len(self.actividades):
        actividad = self.actividades[actividad_index]
        actividad_id = actividad.get("_api_id") or actividad.get("id")
        
        # Intentar eliminar de la API si tiene ID
        if actividad_id:
            print(f"Eliminando actividad de la API: {actividad_id}")
            api_result = ApiService.delete_activity(actividad_id)
            
            if api_result["success"]:
                print(f"Actividad eliminada de la API: {api_result['message']}")
                # Eliminar de la lista local
                self.actividades.pop(actividad_index)
                _update_actividades_container(self)
                if hasattr(self, 'flet_page'):
                    # Mostrar confirmación
                    try:
                        snackbar = ft.SnackBar(
                            ft.Text("✓ Actividad eliminada correctamente", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREEN_700,
                            duration=3000
                        )
                        self.flet_page.overlay.append(snackbar)
                        snackbar.open = True
                    except Exception:
                        pass
                    self.flet_page.update()
            else:
                # Error al eliminar de la API
                print(f"Error al eliminar de la API: {api_result['message']}")
                if hasattr(self, 'flet_page'):
                    try:
                        snackbar = ft.SnackBar(
                            ft.Text(f"Error: {api_result['message']}", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.RED_700,
                            duration=5000
                        )
                        self.flet_page.overlay.append(snackbar)
                        snackbar.open = True
                        self.flet_page.update()
                    except Exception:
                        pass
        else:
            # No tiene ID (actividad local), solo eliminar del local
            self.actividades.pop(actividad_index)
            _update_actividades_container(self)
            if hasattr(self, 'flet_page'):
                self.flet_page.update()

def toggle_completed_actividad(self, actividad_index):
    """
    Marca o desmarca una actividad como completada.
    
    :param actividad_index: Índice de la actividad
    """
    if 0 <= actividad_index < len(self.actividades):
        # Si no existe la clave 'completada', la agregamos
        if 'completada' not in self.actividades[actividad_index]:
            self.actividades[actividad_index]['completada'] = False
        
        # Toggle el estado de completada
        self.actividades[actividad_index]['completada'] = not self.actividades[actividad_index].get('completada', False)
        _update_actividades_container(self)
        self.flet_page.update()

def _update_actividades_container(self):
    """Actualiza el contenedor de actividades con todas las tarjetas."""
    controls = []
    
    # Agregar las tarjetas de actividades
    for actividad in self.actividades:
        card = _create_activity_card(self, actividad)
        controls.append(card)
    
    # Agregar el card de añadir al final
    controls.append(self.add_card)
    
    self.actividades_container.controls = controls

def _create_activity_card(self, actividad_data):
    """
    Crea una tarjeta de actividad basada en los datos proporcionados.
    
    :param actividad_data: Diccionario con los datos de la actividad
    :return: ft.Card con la estructura de la actividad
    """
    # Encontrar el índice de la actividad
    actividad_index = self.actividades.index(actividad_data) if actividad_data in self.actividades else -1
    
    # Verificar si la actividad está completada
    esta_completada = actividad_data.get('completada', False)
    
    # Color del título y strikethrough si está completada
    titulo_color = ft.Colors.GREY_500 if esta_completada else ft.Colors.GREY_800
    titulo_decoration = "line_through" if esta_completada else "none"
    
    return ft.Card(
        width=500,
        content=ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ASSIGNMENT, ft.Colors.INDIGO_ACCENT_400),
                    title=ft.Text(
                        actividad_data.get("titulo", "Sin título"), 
                        weight="bold", 
                        size=20, 
                        color=titulo_color,
                        style=ft.TextStyle(decoration=titulo_decoration)
                    ),
                    subtitle=ft.Text(actividad_data.get("usuario", "[Usuario]"), color=ft.Colors.GREY_600),
                    trailing=ft.Text(actividad_data.get("fecha", "Sin fecha"), color=ft.Colors.GREY_600),
                ),
                
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                    ft.IconButton(
                        ft.Icons.CHECK, 
                        icon_color=ft.Colors.GREEN if esta_completada else ft.Colors.GREY_400,
                        on_click=lambda e, idx=actividad_index: _on_check_click(self, idx)
                    ),
                    ft.PopupMenuButton(items=[
                        ft.PopupMenuItem(
                            text="Editar",
                            on_click=lambda e, idx=actividad_index, data=actividad_data: _on_edit_click(self, idx, data)
                        ),
                        ft.PopupMenuItem(
                            text="Eliminar",
                            on_click=lambda e, idx=actividad_index: _on_delete_click(self, idx)
                        ),
                    ],
                    tooltip="Opciones",
                    )
                ]),
            ]),
            width=400,
            padding=10,
            bgcolor=ft.Colors.GREY_200,
            border_radius=10,
        )
    )

def _on_edit_click(self, actividad_index, actividad_data):
    """
    Maneja el evento de clic del botón editar.
    
    :param actividad_index: Índice de la actividad a editar
    :param actividad_data: Datos de la actividad a editar
    """
    # Establecer los datos a editar en la vista de edición
    if hasattr(self, 'actividades_editar_view'):
        self.actividades_editar_view.set_actividad(actividad_index, actividad_data)
    
    # Navegar a la vista de edición
    if self.change_view:
        self.change_view("actividades_editar")

def _on_delete_click(self, actividad_index):
    """
    Maneja el evento de clic del botón eliminar.
    
    :param actividad_index: Índice de la actividad a eliminar
    """
    delete_actividad(self, actividad_index)

def _on_check_click(self, actividad_index):
    """
    Maneja el evento de clic del botón check (marcar como completado).
    
    :param actividad_index: Índice de la actividad
    """
    toggle_completed_actividad(self, actividad_index)
