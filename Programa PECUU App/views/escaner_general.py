import flet as ft
from components.escaner_general import scan_urls_handler

class EscanerGeneral(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.loading_indicator = ft.ProgressRing(width=30, height=30, stroke_width=4, color=ft.Colors.AMBER)
        self.status_text = ft.Text(value="", size=20)
        self.padding = ft.padding.all(20)
        self.expand = True
        self.bgcolor = ft.Colors.GREY_100
        self.border_radius = 10

        self.scan_button = ft.FilledButton(
            text="ESCANEAR",
            width=200,
            height=50,
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=22, weight="bold")),
        )

        self.results_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.loading_row = ft.Row(
            controls=[self.loading_indicator, self.status_text],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )

        self.content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._create_header(),
                ft.Row(controls=[self.scan_button], alignment=ft.MainAxisAlignment.CENTER),
                self.results_column,
                self.loading_row
            ]
        )

        # Conectar botón al manejador de escaneo
        self.scan_button.on_click = lambda e: scan_urls_handler(
            e,
            self.results_column,
            self.loading_row,
            self.scan_button,
            page,
        )
    
    def _create_header(self):
        return ft.Container(
            padding=ft.padding.only(bottom=20),
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.WIFI_TETHERING, size=30, color=ft.Colors.AMBER),
                            ft.Text(
                                value="ESCANEO GENERAL",
                                size=26,
                                color=ft.Colors.INDIGO_500,
                                weight="bold"
                            )
                        ],
                        spacing=10
                    ),
                    ft.Divider(height=10, color=ft.Colors.GREY_300)
                ]
            )
        )