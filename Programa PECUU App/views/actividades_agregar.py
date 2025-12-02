import flet as ft
from components.inner_header import InnerHeader
from components.actividades_agregar import handle_save

class ActividadesAgregar(ft.Container):
    """
    Representa la vista de "Actividades - Agregar" de la aplicación.

    Hereda de ft.Container y se configura para ocupar toda el área de contenido
    principal de la aplicación.
    """
    def __init__(self, page: ft.Page, change_view=None, add_actividad_callback=None):
        """
        Inicializa la vista y configura todos los componentes de la interfaz.

        :param page: Objeto ft.Page de la aplicación principal.
        :type page: ft.Page
        :param change_view: Función callback para cambiar de vista.
        :type change_view: callable
        :param add_actividad_callback: Función callback para agregar una actividad.
        :type add_actividad_callback: callable
        """
        super().__init__()
        self.page = page
        self.change_view = change_view
        self.add_actividad_callback = add_actividad_callback
        
        # Configuración del contenedor principal de la vista
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_50
        self.border_radius = 10

        self.titulo_textfield = ft.TextField(
            label="Título de la Actividad",
            width=400,
            height=50,
            text_style=ft.TextStyle(size=16),
        )

        self.descripcion_textfield = ft.TextField(
            label="Descripción",
            width=400,
            height=100,
            text_style=ft.TextStyle(size=16),
            multiline=True,
        )

        self.usuario_dropdown = ft.Dropdown(
            label="Usuario Responsable",
            width=400,
            options=[
                ft.dropdown.Option("Usuario 1"),
                ft.dropdown.Option("Usuario 2"),
                ft.dropdown.Option("Usuario 3"),
            ]
        )

        self.fecha_picker = ft.DatePicker(
            on_change=self.on_fecha_change
        )
        self.page.overlay.append(self.fecha_picker)

        self.fecha_display = ft.Text("Seleccionar Fecha", size=16, color=ft.Colors.GREY_600)

        self.save_button = ft.FilledButton(
            text="GUARDAR",
            width=200,
            height=50,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight="bold")),
            on_click=lambda e: handle_save(self, e)
        )

        self.cancel_button = ft.ElevatedButton(
            text="Regresar",
            width=200,
            height=50,
            color=ft.Colors.INDIGO_500,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=18)),
            on_click=lambda e: self.change_view("actividades") if self.change_view else None
        )

        # --- Estructura Principal del Contenido (ft.Column) ---
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                InnerHeader("NUEVA ACTIVIDAD", icon=ft.Icons.ASSIGNMENT_ADD),
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    width=700,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Título:", style=ft.TextStyle(size=16)),
                                self.titulo_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Descripción:", style=ft.TextStyle(size=16)),
                                self.descripcion_textfield
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Usuario:", style=ft.TextStyle(size=16)),
                                self.usuario_dropdown
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Fecha:", style=ft.TextStyle(size=16)),
                                ft.ElevatedButton(
                                    text="Seleccionar Fecha",
                                    on_click=lambda e: self.page.open(self.fecha_picker)
                                ),
                                self.fecha_display
                            ]
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        self.save_button,
                        self.cancel_button
                    ]
                )
            ]
        )

    def on_fecha_change(self, e):
        """Actualiza el texto de fecha mostrado cuando se selecciona una fecha."""
        if e.control.value:
            self.fecha_display.value = e.control.value.strftime("%d/%m/%Y")
            self.page.update()

    async def _navigate_back(self):
        """Navega de vuelta a la vista de actividades."""
        if self.change_view:
            self.change_view("actividades")
