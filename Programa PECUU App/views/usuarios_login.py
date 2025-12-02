import flet as ft
from components.inner_header import InnerHeader

class UsuariosLogin(ft.Container):
    """
    Representa la vista de "Iniciar Sesión" de la aplicación.

    Hereda de ft.Container y se configura para ocupar toda el área de contenido
    principal de la aplicación.
    """
    def __init__(self, page: ft.Page, change_view_callback=None):
        """
        Inicializa la vista y configura todos los componentes de la interfaz.

        :param page: Objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        :param change_view_callback: Función callback para cambiar de vista.
        :type change_view_callback: function
        """
        super().__init__()
        self.page = page
        self.change_view = change_view_callback
        # Configuración del contenedor principal de la vista
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        self.user_icon = ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=150, color=ft.Colors.GREY_500)
        self.username_textfield = self.ddns_textfield = ft.TextField(
            label="Nombre de usuario",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )
        self.password_textfield = self.ddns_textfield = ft.TextField(
            label="Contraseña",
            width=400,
            height=50,
            password=True,
            can_reveal_password=True,
            text_style=ft.TextStyle(size=16),
        )
        
        self.login_button = ft.ElevatedButton(
            "INICIAR SESIÓN", 
            bgcolor=ft.Colors.INDIGO_500, 
            color=ft.Colors.WHITE,
            width=200,
            height=40,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=20, weight="bold")),
            on_click=lambda e: self.change_view("usuarios") if self.change_view else None
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("INICIAR SESIÓN", icon=ft.Icons.ACCOUNT_BOX),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=50,
                    controls=[
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                self.user_icon,
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Usuario:", size=20, color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD),
                            self.username_textfield,
                            ft.Text("Contraseña:", size=20, color=ft.Colors.GREY_800, weight=ft.FontWeight.BOLD),
                            self.password_textfield,
                        ]
                    )]
                ),
                ft.Container(height=20),  # Espaciado vertical
                self.login_button
            ]
        )