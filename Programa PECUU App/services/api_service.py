import requests
import json
from typing import List, Dict, Optional


class ApiService:
    """
    Servicio para conectar con la API de SGCC Backend.
    """
    
    BASE_URL = "https://aids.policiachihuahua.gob.mx/sgcc-backend/api"
    TIMEOUT = 10  # segundos
    
    @staticmethod
    def get_links() -> Optional[List[Dict]]:
        """
        Obtiene la lista de enlaces desde la API.
        
        Returns:
            Lista de diccionarios con los datos de los enlaces.
            Retorna None si hay error en la petición.
        """
        try:
            url = f"{ApiService.BASE_URL}/links.json"
            response = requests.get(url, timeout=ApiService.TIMEOUT, verify=False)
            response.raise_for_status()
            
            data = response.json()
            
            # Transformar los datos de la API al formato esperado por la aplicación
            enlaces = []
            if isinstance(data, list):
                enlaces = data
            elif isinstance(data, dict) and "links" in data:
                enlaces = data["links"]
            elif isinstance(data, dict) and "data" in data:
                enlaces = data["data"]
            
            # Mapear los campos de la API a los campos esperados
            enlaces_formateados = []
            for enlace in enlaces:
                enlace_formateado = {
                    "nombre": enlace.get("nombre") or enlace.get("name") or "",
                    "ddns": enlace.get("ddns") or enlace.get("host") or "",
                    "puerto_http": enlace.get("puerto_http") or enlace.get("http_port") or "",
                    "puerto_rtsp": enlace.get("puerto_rtsp") or enlace.get("rtsp_port") or "",
                }
                enlaces_formateados.append(enlace_formateado)
            
            return enlaces_formateados
            
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
    
    @staticmethod
    def get_link_by_name(nombre: str) -> Optional[Dict]:
        """
        Obtiene un enlace específico por su nombre.
        
        Args:
            nombre: Nombre del enlace a buscar.
            
        Returns:
            Diccionario con los datos del enlace o None si no existe.
        """
        enlaces = ApiService.get_links()
        if enlaces:
            for enlace in enlaces:
                if enlace.get("nombre") == nombre:
                    return enlace
        return None
    
    @staticmethod
    def create_link(enlace_data: Dict) -> Dict:
        """
        Crea un nuevo enlace en la API.
        
        Args:
            enlace_data: Diccionario con los datos del enlace
                Campos esperados:
                - nombre: Nombre del enlace (requerido)
                - ddns: URL/DDNS del enlace (requerido)
                - puerto_http: Puerto HTTP (opcional, default: 80)
                - puerto_rtsp: Puerto RTSP (opcional, default: 554)
                - wifi_nombre: Nombre de la red WiFi (opcional)
                - wifi_password: Contraseña WiFi (opcional)
                - modem_password: Contraseña del módem (opcional)
                - dvr_ip: IP del DVR (opcional)
                - dvr_mac: MAC del DVR (opcional)
        
        Returns:
            Diccionario con el resultado de la operación:
            {
                "success": bool,
                "message": str,
                "data": dict (datos del enlace creado si es exitoso)
            }
        """
        try:
            # Preparar datos para la API
            payload = {
                "nombre": enlace_data.get("nombre"),
                "ddns": enlace_data.get("ddns"),
                "puerto_http": enlace_data.get("puerto_http", "80"),
                "puerto_rtsp": enlace_data.get("puerto_rtsp", "554"),
            }
            
            # Agregar campos opcionales si están presentes
            if enlace_data.get("wifi_nombre"):
                payload["wifi_nombre"] = enlace_data.get("wifi_nombre")
            if enlace_data.get("wifi_password"):
                payload["wifi_password"] = enlace_data.get("wifi_password")
            if enlace_data.get("modem_password"):
                payload["modem_password"] = enlace_data.get("modem_password")
            if enlace_data.get("dvr_ip"):
                payload["dvr_ip"] = enlace_data.get("dvr_ip")
            if enlace_data.get("dvr_mac"):
                payload["dvr_mac"] = enlace_data.get("dvr_mac")
            
            # Realizar petición POST
            url = f"{ApiService.BASE_URL}/links"
            response = requests.post(
                url,
                json=payload,
                timeout=ApiService.TIMEOUT,
                verify=False
            )
            response.raise_for_status()
            
            result_data = response.json()
            
            return {
                "success": True,
                "message": "Enlace creado exitosamente",
                "data": result_data
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error al crear enlace en la API: {e}")
            return {
                "success": False,
                "message": f"Error de conexión: {str(e)}",
                "data": None
            }
        except json.JSONDecodeError as e:
            print(f"Error al decodificar respuesta JSON: {e}")
            return {
                "success": False,
                "message": f"Error al procesar respuesta: {str(e)}",
                "data": None
            }
        except Exception as e:
            print(f"Error inesperado al crear enlace: {e}")
            return {
                "success": False,
                "message": f"Error inesperado: {str(e)}",
                "data": None
            }
    
    @staticmethod
    def update_link(nombre: str, enlace_data: Dict) -> Dict:
        """
        Actualiza un enlace existente en la API.
        
        Args:
            nombre: Nombre del enlace a actualizar
            enlace_data: Diccionario con los datos actualizados
        
        Returns:
            Diccionario con el resultado de la operación
        """
        try:
            # Preparar datos para la API
            payload = {
                "nombre": enlace_data.get("nombre", nombre),
                "ddns": enlace_data.get("ddns"),
                "puerto_http": enlace_data.get("puerto_http", "80"),
                "puerto_rtsp": enlace_data.get("puerto_rtsp", "554"),
            }
            
            # Agregar campos opcionales si están presentes
            if enlace_data.get("wifi_nombre"):
                payload["wifi_nombre"] = enlace_data.get("wifi_nombre")
            if enlace_data.get("wifi_password"):
                payload["wifi_password"] = enlace_data.get("wifi_password")
            if enlace_data.get("modem_password"):
                payload["modem_password"] = enlace_data.get("modem_password")
            if enlace_data.get("dvr_ip"):
                payload["dvr_ip"] = enlace_data.get("dvr_ip")
            if enlace_data.get("dvr_mac"):
                payload["dvr_mac"] = enlace_data.get("dvr_mac")
            
            # Realizar petición PUT
            url = f"{ApiService.BASE_URL}/links/{nombre}"
            response = requests.put(
                url,
                json=payload,
                timeout=ApiService.TIMEOUT,
                verify=False
            )
            response.raise_for_status()
            
            result_data = response.json()
            
            return {
                "success": True,
                "message": "Enlace actualizado exitosamente",
                "data": result_data
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar enlace en la API: {e}")
            return {
                "success": False,
                "message": f"Error de conexión: {str(e)}",
                "data": None
            }
        except Exception as e:
            print(f"Error inesperado al actualizar enlace: {e}")
            return {
                "success": False,
                "message": f"Error inesperado: {str(e)}",
                "data": None
            }
    
    @staticmethod
    def delete_link(nombre: str) -> Dict:
        """
        Elimina un enlace de la API.
        
        Args:
            nombre: Nombre del enlace a eliminar
        
        Returns:
            Diccionario con el resultado de la operación
        """
        try:
            url = f"{ApiService.BASE_URL}/links/{nombre}"
            response = requests.delete(
                url,
                timeout=ApiService.TIMEOUT,
                verify=False
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "message": "Enlace eliminado exitosamente",
                "data": None
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar enlace en la API: {e}")
            return {
                "success": False,
                "message": f"Error de conexión: {str(e)}",
                "data": None
            }
        except Exception as e:
            print(f"Error inesperado al eliminar enlace: {e}")
            return {
                "success": False,
                "message": f"Error inesperado: {str(e)}",
                "data": None
            }
