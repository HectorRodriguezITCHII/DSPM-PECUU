import flet as ft
import asyncio
from services.api_service import ApiService

def handle_save(self, e):
    """
    Manejador del evento de clic del botón guardar para una nueva actividad.
    Valida los campos requeridos y guarda la actividad en la API.
        
    :param self: Instancia de ActividadesAgregar
    :param e: Evento de clic.
    """
    # Validar que los campos obligatorios no estén vacíos
    if not self.titulo_textfield.value:
        # Mostrar alerta si falta el título
        snackbar = ft.SnackBar(
            content=ft.Text("Por favor, ingresa un título para la actividad", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_400
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()
        return
        
    # Crear diccionario con los datos de la actividad
    actividad_data = {
        "titulo": self.titulo_textfield.value,
        "descripcion": self.descripcion_textfield.value or "",
        "usuario": self.usuario_dropdown.value or "",
        "fecha": self.fecha_display.value or "Sin fecha",
    }
    
    # Intentar crear la actividad en la API
    print(f"Creando actividad: {actividad_data['titulo']}")
    api_result = ApiService.create_activity(actividad_data)
    
    if api_result["success"]:
        print(f"Actividad creada: {api_result['message']}")
        
        # Llamar al callback para agregar la actividad localmente
        if self.add_actividad_callback:
            self.add_actividad_callback(actividad_data)
        
        # Limpiar los campos
        self.titulo_textfield.value = ""
        self.descripcion_textfield.value = ""
        self.usuario_dropdown.value = None
        self.fecha_display.value = "Seleccionar Fecha"
        
        # Mostrar mensaje de éxito con Snackbar
        try:
            snackbar = ft.SnackBar(
                ft.Text("✓ Actividad creada exitosamente", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
                duration=3000
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()
        except Exception as ex:
            print(f"Error showing snackbar: {ex}")
        
        # Regresar a la vista de actividades
        if self.change_view:
            self.change_view("actividades")
    else:
        # Mostrar error
        print(f"Error al crear actividad: {api_result['message']}")
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
