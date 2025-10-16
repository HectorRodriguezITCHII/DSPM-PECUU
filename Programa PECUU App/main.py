import flet as ft
from components.header import Header
from components.menu import Menu
from views.escaner_general import EscanerGeneral

class MainApp(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.page.title = "Sistema de Gestión de Cámaras Ciudadanas"
        self.page.bgcolor = ft.Colors.GREY_100
        
        #componentes
        self.header = Header(page)
        self.menu = Menu(page)
        
        #vistas
        self.views = {
            "escaner_general": EscanerGeneral(page),
        }
        
        #configurar eventos del menu
        self.setup_menu_events()
        
        #vista actual
        self.current_view = self.views["escaner_general"]
        
        #cuerpo principal
        self.body = ft.Container(
            expand=True,
            content=ft.Row(
                controls=[
                    self.menu,
                    self.current_view
                ]
            )
        )
        
        #diseño principal
        self.page.add(ft.Column(
            expand=True,
            controls=[
                self.header,
                self.body
            ]
        ))
    
    def setup_menu_events(self):
        #configurar los eventos delos botones del menu
        self.menu.inicio_btn.on_click = lambda e: self.change_view("inicio")
        self.menu.escaner_general_btn.on_click = lambda e: self.change_view("escaner_general")
        self.menu.escaner_local_btn.on_click = lambda e: self.change_view("escaner_local")
        self.menu.enlaces_btn.on_click = lambda e: self.change_view("enlaces")
        self.menu.historial_btn.on_click = lambda e: self.change_view("historial")
        
    def change_view(self, view_name):
        self.body.content.controls[1] = self.views.get(view_name, ft.Text("Vista no disponible"))
        if view_name == "inicio":
            self.menu.inicio_btn.icon_color = ft.Colors.BLUE_800
            self.menu.escaner_general_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_local_btn.icon_color = ft.Colors.BLUE_400
            self.menu.enlaces_btn.icon_color = ft.Colors.BLUE_400
            self.menu.historial_btn.icon_color = ft.Colors.BLUE_400
        elif view_name == "escaner_general":
            self.menu.inicio_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_general_btn.icon_color = ft.Colors.BLUE_800
            self.menu.escaner_local_btn.icon_color = ft.Colors.BLUE_400
            self.menu.enlaces_btn.icon_color = ft.Colors.BLUE_400
            self.menu.historial_btn.icon_color = ft.Colors.BLUE_400
        elif view_name == "escaner_local":
            self.menu.inicio_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_general_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_local_btn.icon_color = ft.Colors.BLUE_800
            self.menu.enlaces_btn.icon_color = ft.Colors.BLUE_400
            self.menu.historial_btn.icon_color = ft.Colors.BLUE_400
        elif view_name == "enlaces":
            self.menu.inicio_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_general_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_local_btn.icon_color = ft.Colors.BLUE_400
            self.menu.enlaces_btn.icon_color = ft.Colors.BLUE_800
            self.menu.historial_btn.icon_color = ft.Colors.BLUE_400
        elif view_name == "historial":
            self.menu.inicio_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_general_btn.icon_color = ft.Colors.BLUE_400
            self.menu.escaner_local_btn.icon_color = ft.Colors.BLUE_400
            self.menu.enlaces_btn.icon_color = ft.Colors.BLUE_400
            self.menu.historial_btn.icon_color = ft.Colors.BLUE_800
        