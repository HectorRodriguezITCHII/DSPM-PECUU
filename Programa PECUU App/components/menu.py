import flet as ft

class Menu(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(width=60, border_radius=10, padding=5)
        # store page if needed for updates
        self.page = page
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.INDIGO_100, ft.Colors.INDIGO_600],
        )

        # guardar los iconos como atributos (inicialmente outlined cuando existe)
        self.inicio_btn = ft.IconButton(icon=ft.Icons.HOME_OUTLINED, tooltip="Inicio", icon_color=ft.Colors.INDIGO_500)
        self.escaner_general_btn = ft.IconButton(icon=ft.Icons.WIFI_TETHERING_OUTLINED, tooltip="Escaneo General", icon_color=ft.Colors.INDIGO_400)
        self.escaner_local_btn = ft.IconButton(icon=ft.Icons.ROUTER_OUTLINED, tooltip="Escaneo Local", icon_color=ft.Colors.INDIGO_400)
        self.enlaces_btn = ft.IconButton(icon=ft.Icons.HUB_OUTLINED, tooltip="Enlaces", icon_color=ft.Colors.INDIGO_400)
        self.historial_btn = ft.IconButton(icon=ft.Icons.HISTORY_OUTLINED, tooltip="Historial", icon_color=ft.Colors.INDIGO_400)
        # Ajustes puede no tener variante outlined; mantener SETTINGS como fallback
        self.ajustes_btn = ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Ajustes", icon_color=ft.Colors.INDIGO_50)

        # mapa explícito de iconos (outline, filled). Si la variante filled no existe, se usa el mismo icono.
        self._icon_map = {
            "inicio": (ft.Icons.HOME_OUTLINED, getattr(ft.Icons, "HOME", ft.Icons.HOME_OUTLINED)),
            "escaner_general": (ft.Icons.WIFI_TETHERING_OUTLINED, getattr(ft.Icons, "WIFI_TETHERING", ft.Icons.WIFI_TETHERING_OUTLINED)),
            "escaner_local": (ft.Icons.ROUTER_OUTLINED, getattr(ft.Icons, "ROUTER", ft.Icons.ROUTER_OUTLINED)),
            "enlaces": (ft.Icons.HUB_OUTLINED, getattr(ft.Icons, "HUB", ft.Icons.HUB_OUTLINED)),
            "historial": (ft.Icons.HISTORY_OUTLINED, getattr(ft.Icons, "HISTORY", ft.Icons.HISTORY_OUTLINED)),
            "ajustes": (ft.Icons.SETTINGS, getattr(ft.Icons, "SETTINGS", ft.Icons.SETTINGS)),
        }

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    controls=[
                        self.inicio_btn,
                        self.escaner_general_btn,
                        self.escaner_local_btn,
                        self.enlaces_btn,
                        self.historial_btn,
                    ]
                ),
                ft.Column(
                    controls=[
                        self.ajustes_btn,
                    ]
                ),
            ]
        )

    def set_selected(self, view_name: str):
        """Cambiar los iconos a su versión filled para la vista seleccionada y ajustar colores.

        - view_name: nombre de la vista (ej: 'inicio', 'escaner_general', ...)
        """
        # helper to switch icon if a filled version exists
        def filled_icon(icon_data):
            try:
                # get the name of the icon constant, try to remove _OUTLINED
                name = icon_data.name
            except Exception:
                # fallback: can't determine, return original
                return icon_data

            if name.endswith("_OUTLINED"):
                filled_name = name.replace("_OUTLINED", "")
            else:
                filled_name = name

            # return the filled icon if it exists in ft.Icons, otherwise original
            return getattr(ft.Icons, filled_name, icon_data)

        # default all to unselected color
        default_color = ft.Colors.INDIGO_300
        selected_color = ft.Colors.WHITE

        # map view to the button object
        btn_map = {
            "inicio": self.inicio_btn,
            "escaner_general": self.escaner_general_btn,
            "escaner_local": self.escaner_local_btn,
            "enlaces": self.enlaces_btn,
            "historial": self.historial_btn,
            "ajustes": self.ajustes_btn,
        }

        # iterate and set icon/color
        for name, btn in btn_map.items():
            # set filled icon for selected, keep outlined/regular for others
            if name == view_name:
                btn.icon = filled_icon(btn.icon)
                btn.icon_color = selected_color
            else:
                # restore to outlined if original had outlined in its name
                # We attempt to find an outlined variant by appending _OUTLINED
                try:
                    icon_name = btn.icon.name
                except Exception:
                    icon_name = None

                if icon_name and not icon_name.endswith("_OUTLINED"):
                    outlined_name = icon_name + "_OUTLINED"
                    btn.icon = getattr(ft.Icons, outlined_name, btn.icon)

                btn.icon_color = default_color

        # small UI refresh
        try:
            self.update()
        except Exception:
            # if update not available, try to update page
            try:
                if hasattr(self, "page"):
                    self.page.update()
            except Exception:
                pass