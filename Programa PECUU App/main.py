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
        "escaner_general": EscanerGeneral(page)
        
        
        
        

'''def main(page: ft.Page):
    page.bgcolor = ft.Colors.GREY_200
    page.title = "Sistema de Gestión de Cámaras Ciudadanas"
    page.padding = ft.padding.symmetric(20, 10)
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    text_title, img_logo_white, bottom_bar = setup_ui(page)
    
    page.appbar = ft.AppBar(
        leading=img_logo_white,
        leading_width=150,
        title=text_title,
        center_title=False,
        toolbar_height=60,
        bgcolor=ft.Colors.BLUE_GREY_500,
        elevation=8,
        shadow_color=ft.Colors.BLACK38,
        actions=[
            ft.IconButton(ft.Icons.ACCOUNT_CIRCLE, icon_color=ft.Colors.WHITE, icon_size=30, tooltip="Usuarios"),
            ft.IconButton(ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE, icon_size=30, tooltip="Configuración")
        ],
    )
    
    page.add(
        bottom_bar
    )

ft.app(target=main)'''