import flet as ft

class Menu(ft.Container):
    """
    Componente de menú de navegación lateral.

    Hereda de ft.Container y está diseñado para ser la barra de navegación vertical, 
    gestionando los botones que cambian las vistas de la aplicación principal 
    (MainApp).
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa el menú, configura su estilo visual (gradiente) y define 
        los botones de navegación con sus íconos por defecto (outlined).

        :param page: El objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        """
        super().__init__(width=60, border_radius=10, padding=5)
        self.page = page
        
        # Gradiente visual aplicado al fondo del contenedor del menú
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.INDIGO_100, ft.Colors.INDIGO_ACCENT_700],
        )

        # --- Definición de Botones de Navegación ---
        # Se definen todos los botones como atributos para ser accedidos externamente 
        # (ej. para asignar eventos on_click en MainApp).
        self.inicio_btn = ft.IconButton(
            icon=ft.Icons.HOME, 
            tooltip="Inicio", 
            icon_color=ft.Colors.YELLOW_100,
            hover_color=ft.Colors.INDIGO_200
        )
        
        self.escaner_general_btn = ft.IconButton(
            icon=ft.Icons.WIFI_TETHERING_OUTLINED, 
            tooltip="Escaneo General", 
            icon_color=ft.Colors.INDIGO_500,
            hover_color=ft.Colors.INDIGO_200
        )
        
        self.escaner_local_btn = ft.IconButton(
            icon=ft.Icons.ROUTER_OUTLINED, 
            tooltip="Escaneo Local", 
            icon_color=ft.Colors.INDIGO_500,
            hover_color=ft.Colors.INDIGO_300
        )
        
        self.enlaces_btn = ft.IconButton(
            icon=ft.Icons.HUB_OUTLINED, 
            tooltip="Enlaces", 
            icon_color=ft.Colors.INDIGO_500,
            hover_color=ft.Colors.INDIGO_300
        )

        self.historial_btn = ft.IconButton(
            icon=ft.Icons.HISTORY_OUTLINED, 
            tooltip="Historial", 
            icon_color=ft.Colors.INDIGO_500,
            hover_color=ft.Colors.INDIGO_300
        )
        
        # Botón de Usuario (icon_color diferente para destacarlo como acción secundaria)
        self.usuarios_btn = ft.IconButton(
            icon=ft.Icons.ACCOUNT_CIRCLE,
            icon_color=ft.Colors.WHITE,
            hover_color=ft.Colors.INDIGO_500,
            tooltip="Usuarios"
        )

        # --- Mapa de Iconos (Gestión de Estado) ---
        # Mapa interno para referenciar las variantes outlined y filled de cada icono.
        self._icon_map = {
            # El uso de getattr(ft.Icons, "NOMBRE", FALLBACK) permite manejar 
            # casos donde no existe la variante 'filled' del icono.
            "inicio": (ft.Icons.HOME_OUTLINED, getattr(ft.Icons, "HOME", ft.Icons.HOME_OUTLINED)),
            "escaner_general": (ft.Icons.WIFI_TETHERING_OUTLINED, getattr(ft.Icons, "WIFI_TETHERING", ft.Icons.WIFI_TETHERING_OUTLINED)),
            "escaner_local": (ft.Icons.ROUTER_OUTLINED, getattr(ft.Icons, "ROUTER", ft.Icons.ROUTER_OUTLINED)),
            "enlaces": (ft.Icons.HUB_OUTLINED, getattr(ft.Icons, "HUB", ft.Icons.HUB_OUTLINED)),
            "historial": (ft.Icons.HISTORY_OUTLINED, getattr(ft.Icons, "HISTORY", ft.Icons.HISTORY_OUTLINED)),
            "usuarios": (ft.Icons.ACCOUNT_CIRCLE_OUTLINED, getattr(ft.Icons, "ACCOUNT_CIRCLE", ft.Icons.ACCOUNT_CIRCLE_OUTLINED)),
        }

        # --- Estructura del Contenido ---
        # Dos columnas separadas: una para los botones principales y otra para Ajustes (abajo).
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Coloca los dos grupos en extremos opuestos
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column( # Grupo superior de navegación
                    controls=[
                        self.inicio_btn,
                        self.escaner_general_btn,
                        self.escaner_local_btn,
                        self.enlaces_btn,
                        self.historial_btn,
                    ]
                ),
                ft.Column( # Grupo inferior (Usuarios)
                    controls=[
                        self.usuarios_btn,
                    ]
                ),
            ]
        )

    def set_selected(self, view_name: str):
        """
        Actualiza el estado visual del menú, marcando la vista seleccionada.

        La vista seleccionada se identifica cambiando su ícono a la variante 
        'filled' (si está disponible) y su color a amarillo (ft.Colors.YELLOW_100), 
        mientras que el resto de los botones se restablecen a su estado 'outlined' 
        y color por defecto (ft.Colors.INDIGO_500).

        :param view_name: Nombre (clave) de la vista seleccionada (ej: 'inicio').
        :type view_name: str
        """
        # Función auxiliar para intentar obtener la variante 'filled' del ícono
        def filled_icon(icon_data):
            try:
                name = icon_data.name
            except Exception:
                return icon_data

            # Lógica para quitar el sufijo "_OUTLINED"
            filled_name = name.replace("_OUTLINED", "")

            # Retorna el ícono 'filled' si existe, sino retorna el original
            return getattr(ft.Icons, filled_name, icon_data)

        # Colores
        default_color = ft.Colors.INDIGO_500
        selected_color = ft.Colors.YELLOW_100

        # Mapeo de nombres de vista a objetos de botón para fácil iteración
        btn_map = {
            "inicio": self.inicio_btn,
            "escaner_general": self.escaner_general_btn,
            "escaner_local": self.escaner_local_btn,
            "enlaces": self.enlaces_btn,
            "historial": self.historial_btn,
        }

        # Iterar sobre los botones principales y actualizar su estado
        for name, btn in btn_map.items():
            if name == view_name:
                # Estado SELECCIONADO: cambiar a icono lleno y color resaltado
                btn.icon = filled_icon(btn.icon)
                btn.icon_color = selected_color
            else:
                # Estado NO SELECCIONADO: restablecer a icono outline y color por defecto
                try:
                    icon_name = btn.icon.name
                except Exception:
                    icon_name = None

                # Si el icono actual NO tiene sufijo OUTLINED, añadirlo (restablecer)
                if icon_name and not icon_name.endswith("_OUTLINED"):
                    outlined_name = icon_name + "_OUTLINED"
                    btn.icon = getattr(ft.Icons, outlined_name, btn.icon)

                btn.icon_color = default_color

        # Actualizar la UI de Flet para reflejar los cambios
        try:
            self.update() # Intentar actualizar el control directamente
        except Exception:
            try:
                if hasattr(self, "page"):
                    self.page.update() # Fallback: forzar actualización de la página
            except Exception:
                pass