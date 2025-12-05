# Integración API de Enlaces

## Descripción

Se ha integrado completamente la API de SGCC Backend (`https://aids.policiachihuahua.gob.mx/sgcc-backend/api/links.json`) con la vista de Enlaces de la aplicación PECUU. La integración incluye:
- ✅ Lectura de enlaces (GET)
- ✅ Creación de enlaces (POST)
- ✅ Actualización de enlaces (PUT)
- ✅ Eliminación de enlaces (DELETE)

## Archivos Creados/Modificados

### 1. `services/api_service.py` (NUEVO)
Servicio que gestiona la conexión con la API de SGCC Backend.

**Métodos principales:**

#### GET - Lectura
- `get_links()`: Obtiene la lista completa de enlaces desde la API
  - Transforma los datos de la API al formato esperado por la aplicación
  - Maneja diferentes estructuras de respuesta JSON
  - Retorna `None` si hay error

- `get_link_by_name(nombre)`: Obtiene un enlace específico por su nombre

#### POST - Creación
- `create_link(enlace_data)`: Crea un nuevo enlace en la API
  ```python
  enlace_data = {
      "nombre": "Cámara 1",
      "ddns": "camera1.dyndns.org",
      "puerto_http": "8080",
      "puerto_rtsp": "554",
      "wifi_nombre": "Mi WiFi",
      "wifi_password": "contraseña",
      "modem_password": "contraseña",
      "dvr_ip": "192.168.1.100",
      "dvr_mac": "00:1A:2B:3C:4D:5E"
  }
  result = ApiService.create_link(enlace_data)
  ```
  Retorna:
  ```python
  {
      "success": True/False,
      "message": "Mensaje descriptivo",
      "data": {...}  # Datos del enlace creado si es exitoso
  }
  ```

#### PUT - Actualización
- `update_link(nombre, enlace_data)`: Actualiza un enlace existente en la API
  ```python
  new_data = {
      "nombre": "Cámara 1 Actualizada",
      "ddns": "camera1-new.dyndns.org"
  }
  result = ApiService.update_link("Cámara 1", new_data)
  ```

#### DELETE - Eliminación
- `delete_link(nombre)`: Elimina un enlace de la API
  ```python
  result = ApiService.delete_link("Cámara 1")
  ```

**Características:**
- Manejo robusto de errores (excepciones de conexión, JSON, etc.)
- Mapeo flexible de campos (soporta múltiples nombres de campos)
- Timeout de 10 segundos para las peticiones
- Retorna respuestas consistentes con estructura `{success, message, data}`

### 2. `components/enlaces_agregar.py` (MODIFICADO)
Se actualizó la función `handle_save()` para:
- Crear el enlace en la API usando `ApiService.create_link()`
- Mostrar mensajes de éxito o error
- Solo actualizar la tabla local si la API confirma la creación
- Manejar excepciones de conexión de forma elegante

### 3. `components/enlaces.py` (MODIFICADO)
Se actualizó el método `delete_row()` para:
- Eliminar el enlace de la API usando `ApiService.delete_link()`
- Mostrar mensajes de éxito o error
- Solo eliminar de la tabla local si la API confirma la eliminación

### 4. `views/enlaces.py` (MODIFICADO)
Se mantienen los métodos para cargar datos desde la API

## Flujo de Datos

### Lectura de Enlaces
```
1. La vista Enlaces se inicializa
   ↓
2. Se llama a load_enlaces_from_api()
   ↓
3. ApiService.get_links() realiza la petición HTTP GET
   ↓
4. Los datos se transforman al formato esperado
   ↓
5. EnlacesManager.add_enlace() agrega cada enlace a la tabla
```

### Creación de Enlace
```
1. Usuario llena el formulario en "Nuevo Enlace"
   ↓
2. Usuario hace clic en "Guardar"
   ↓
3. handle_save() valida los datos
   ↓
4. ApiService.create_link() realiza la petición HTTP POST
   ↓
5. Si es exitoso:
   - El enlace se agrega a la tabla local
   - Se muestra mensaje de éxito
   - Se regresa a la vista de enlaces
   ↓
6. Si hay error:
   - Se muestra mensaje de error
   - El usuario puede reintentar
```

### Eliminación de Enlace
```
1. Usuario hace clic en el botón de eliminar en la tabla
   ↓
2. EnlacesManager.delete_row() se ejecuta
   ↓
3. ApiService.delete_link() realiza la petición HTTP DELETE
   ↓
4. Si es exitoso:
   - El enlace se elimina de la tabla
   - Se muestra mensaje de éxito
   ↓
5. Si hay error:
   - Se muestra mensaje de error
   - El enlace se mantiene en la tabla
```

## Estructura de Datos Esperada

### Formato de entrada de la API:
```json
[
  {
    "nombre": "Cámara 1",
    "ddns": "example.dyndns.org",
    "puerto_http": 8080,
    "puerto_rtsp": 554,
    "wifi_nombre": "Mi WiFi",
    "wifi_password": "contraseña",
    "modem_password": "contraseña",
    "dvr_ip": "192.168.1.100",
    "dvr_mac": "00:1A:2B:3C:4D:5E"
  }
]
```

### Formato esperado por la aplicación:
```python
{
    "nombre": "Cámara 1",
    "ddns": "example.dyndns.org",
    "puerto_http": "8080",
    "puerto_rtsp": "554",
    "wifi_nombre": "Mi WiFi",
    "wifi_password": "contraseña",
    "modem_password": "contraseña",
    "dvr_ip": "192.168.1.100",
    "dvr_mac": "00:1A:2B:3C:4D:5E"
}
```

## Uso

### Cargar datos automáticamente:
Los datos se cargan automáticamente cuando se crea la instancia de la vista `Enlaces`.

### Crear nuevo enlace:
1. Hacer clic en botón "Añadir" en la vista de Enlaces
2. Completar el formulario
3. Hacer clic en "GUARDAR"
4. El enlace se crea en la API y se muestra en la tabla

### Eliminar enlace:
1. En la tabla de Enlaces, hacer clic en el icono de eliminar (🗑️)
2. El enlace se elimina de la API
3. La tabla se actualiza automáticamente

### Refrescar datos manualmente:
```python
# Desde cualquier parte de la aplicación que tenga acceso a la vista
enlaces_view.refresh_enlaces_from_api()
```

## Manejo de Errores

- Si la API no está disponible durante la lectura, la tabla se muestra vacía
- Si hay error al crear un enlace, se muestra un mensaje descriptivo y se permite reintentar
- Si hay error al eliminar, se muestra un mensaje y el enlace se mantiene en la tabla
- Todos los errores se imprimen en la consola para debugging
- Se muestra un Snackbar con el estado (éxito o error) de cada operación

## Requisitos

Se necesita instalar el paquete `requests`:
```bash
pip install requests
```

## Configuración Opcional

### Cambiar la URL base de la API:
Edita `services/api_service.py`:
```python
BASE_URL = "https://nueva-url.com/api"
```

### Cambiar el timeout de las peticiones:
```python
TIMEOUT = 20  # segundos
```

## Notas de Seguridad

La API usa HTTPS. Para desarrollo local sin certificados válidos, el código actual usa `verify=False`. 
En producción, asegúrate de usar certificados válidos.

## Ejemplo de Uso Completo

```python
# Obtener todos los enlaces
enlaces = ApiService.get_links()
print(f"Total de enlaces: {len(enlaces)}")

# Crear un nuevo enlace
new_link = {
    "nombre": "Nueva Cámara",
    "ddns": "nuevacamera.dyndns.org",
    "puerto_http": "8080",
    "puerto_rtsp": "554"
}
result = ApiService.create_link(new_link)
if result["success"]:
    print("Enlace creado exitosamente")
else:
    print(f"Error: {result['message']}")

# Buscar un enlace específico
enlace = ApiService.get_link_by_name("Nueva Cámara")
if enlace:
    print(f"Encontrado: {enlace}")

# Actualizar un enlace
updated_data = {
    "nombre": "Nueva Cámara Actualizada",
    "puerto_http": "9090"
}
result = ApiService.update_link("Nueva Cámara", updated_data)
if result["success"]:
    print("Enlace actualizado")

# Eliminar un enlace
result = ApiService.delete_link("Nueva Cámara Actualizada")
if result["success"]:
    print("Enlace eliminado")
```

