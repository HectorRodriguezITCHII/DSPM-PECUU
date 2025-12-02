import flet as ft


class EnlacesManager:
    @staticmethod
    def add_enlace(view: ft.Container, enlace_data: dict):
        """Agrega una fila a la data_table de la vista "Enlaces".

        view: instancia de la vista `Enlaces` (ft.Container)
        enlace_data: diccionario con llaves 'nombre','ddns','puerto_http','puerto_rtsp'
        """
        # create buttons without binding click yet; bind after row is created so we
        # can attach the enlace_data reference to the row and keep it in sync
        inspect_btn = ft.IconButton(
            icon=ft.Icons.VISIBILITY,
            icon_color=ft.Colors.INDIGO_ACCENT_400,
            tooltip="Inspeccionar",
            on_click=None
        )

        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_ACCENT_400,
            tooltip="Eliminar",
            on_click=None
        )

        new_row = ft.DataRow(
            cells=[
                ft.DataCell(inspect_btn),
                ft.DataCell(ft.Text(enlace_data.get("nombre", ""), style=view.text_style)),
                ft.DataCell(ft.Text(enlace_data.get("ddns", ""), style=view.text_style)),
                ft.DataCell(ft.Text(enlace_data.get("puerto_http", ""), style=view.text_style)),
                ft.DataCell(ft.Text(enlace_data.get("puerto_rtsp", ""), style=view.text_style)),
                ft.DataCell(delete_btn),
            ]
        )

        # attach the original data dict to the row so updates mutate the same object
        new_row._enlace_data = enlace_data

        # bind button callbacks referencing the attached data
        inspect_btn.on_click = lambda e, data=new_row._enlace_data: EnlacesManager.open_inspect_view(view, data)
        delete_btn.on_click = lambda e, data=new_row._enlace_data: EnlacesManager.delete_row(view, data)

        view.data_table.rows.append(new_row)
        # actualizar vista
        if hasattr(view, "page") and view.page and hasattr(view.page, "update"):
            view.page.update()

    @staticmethod
    def open_inspect_view(view: ft.Container, enlace_data: dict):
        """Crear la vista de inspección para el enlace y navegar hacia ella.

        Si la vista tiene `change_view` callable, lo usa para cambiar.
        De lo contrario intenta acceder a view.page y actualizar directamente.
        """
        # Import EnlacesInspeccionar lazily to avoid circular import at module load time
        try:
            from views.enlaces_inspeccionar import EnlacesInspeccionar
        except Exception:
            EnlacesInspeccionar = None

        if EnlacesInspeccionar:
            inspect_view = EnlacesInspeccionar(view.page if hasattr(view, 'page') else None, change_view=getattr(view, 'change_view', None), enlace_data=enlace_data)
            # Adjuntar referencia a la vista origen para poder actualizarla al guardar
            inspect_view._source_view = view
            # Preferir usar el callback change_view si está disponible
            if hasattr(view, 'change_view') and callable(view.change_view):
                view.change_view(inspect_view)
            else:
                # Si no hay callback, intentar reemplazar directamente (no ideal)
                if hasattr(view, 'page') and view.page:
                    try:
                        view.page.update()
                    except Exception:
                        pass
        else:
            # Fallback: si no se puede importar, intentar usar change_view con raw data
            if hasattr(view, 'change_view') and callable(view.change_view):
                view.change_view({'inspect_data': enlace_data})
            elif hasattr(view, 'page') and view.page:
                try:
                    view.page.add(ft.Text('No se pudo abrir la vista de inspección.'))
                    view.page.update()
                except Exception:
                    pass

    @staticmethod
    def update_enlace(source_view: ft.Container, original_name: str, new_data: dict):
        """Actualiza la fila cuyo nombre coincide con original_name usando new_data."""
        for row in source_view.data_table.rows:
            cell = row.cells[1]
            text = None
            if hasattr(cell, 'content') and hasattr(cell.content, 'value'):
                text = cell.content.value
            if text == original_name:
                # actualizar celdas
                row.cells[1].content.value = new_data.get('nombre', text)
                row.cells[2].content.value = new_data.get('ddns', row.cells[2].content.value)
                row.cells[3].content.value = new_data.get('puerto_http', row.cells[3].content.value)
                row.cells[4].content.value = new_data.get('puerto_rtsp', row.cells[4].content.value)
                # also update the attached enlace_data dict if present
                try:
                    if hasattr(row, '_enlace_data') and isinstance(row._enlace_data, dict):
                        row._enlace_data.update(new_data)
                except Exception:
                    pass
                # actualizar visual
                if hasattr(source_view, 'page') and source_view.page and hasattr(source_view.page, 'update'):
                    source_view.page.update()
                break

    @staticmethod
    def delete_row(view: ft.Container, enlace_data: dict):
        """Elimina la fila de la data_table que coincide con enlace_data['nombre']"""
        for row in list(view.data_table.rows):
            # row.cells[1] es ft.DataCell con un ft.Text en content
            cell = row.cells[1]
            text = None
            if hasattr(cell, 'content') and hasattr(cell.content, 'value'):
                text = cell.content.value
            if text == enlace_data.get("nombre"):
                view.data_table.rows.remove(row)
                if hasattr(view, "page") and view.page and hasattr(view.page, "update"):
                    view.page.update()
                break
