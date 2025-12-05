# Actualización: Escaneo General solo de DDNS desde la API

## 📋 Cambios Realizados

He modificado el **Escáner General** para que:

### ✅ Antes (Comportamiento Anterior)
- Escaneaba una lista fija de 200+ URLs predefinidas en el código
- No se actualizaba dinámicamente
- Buscaba solo URLs SIN puertos abiertos

### ✅ Ahora (Comportamiento Nuevo)
- **Obtiene dinámicamente los DDNS desde la API** de SGCC Backend
- Extrae solo el campo `ddns` de cada enlace
- Escanea solo los DDNS configurados en la API
- Muestra estado de cada escaneo (abierto/cerrado/error)
- Se actualiza automáticamente cuando hay nuevos enlaces en la API

## 🔧 Cambios en `components/escaner_general.py`

### 1. Importación de ApiService
```python
from services.api_service import ApiService
```

### 2. Eliminación de lista predefinida
```python
# Antes: 200+ URLs codificadas
# Ahora: Lista vacía (datos vienen de la API)
PREDEFINED_URLS = []
```

### 3. Nueva lógica en `scan_urls_handler()`

**Obtener DDNS de la API:**
```python
enlaces = ApiService.get_links()
urls = [enlace.get("ddns", "") for enlace in enlaces if enlace.get("ddns")]
```

**Presentación de resultados mejorada:**
- Verde: DDNS con puertos abiertos ✓
- Gris: DDNS sin puertos abiertos
- Rojo: Error en resolución DNS

## 🔄 Flujo de Escaneo

```
1. Usuario hace click en "ESCANEAR"
   ↓
2. Se cargan DDNS desde la API
   ↓
3. Se resuelven a IP direcciones
   ↓
4. Se escanean puertos en cada IP
   ↓
5. Se muestran resultados detallados
```

## 📊 Información Mostrada

Para cada DDNS se muestra:
- **DDNS/URL**: Nombre del enlace
- **IP**: Dirección IP resuelta
- **Puertos abiertos**: Lista de puertos disponibles
- **Puertos cerrados**: Lista de puertos sin respuesta
- **Estado**: Éxito o error de conexión

## ⚠️ Manejo de Errores

- **API no disponible**: Mensaje informativo al usuario
- **DDNS sin resolver**: Muestra error de DNS
- **Error de conexión**: Captura y muestra el error
- **DDNS vacíos**: Se ignoran automáticamente

## 🚀 Ventajas

✅ Datos siempre sincronizados con la API
✅ No requiere mantenimiento de lista de URLs
✅ Escalable: funciona con cualquier cantidad de enlaces
✅ Información completa de puertos
✅ Mejor manejo de errores

## 📝 Ejemplo de Uso

El usuario simplemente hace click en "ESCANEAR" y:
1. Se obtienen automáticamente todos los DDNS de la API
2. Se escanean todos los puertos configurados
3. Se muestra un informe detallado con los resultados

## 🔗 API Utilizada

Endpoint: `https://aids.policiachihuahua.gob.mx/sgcc-backend/api/links.json`

Datos obtenidos:
```json
{
  "nombre": "Plaza del Sol",
  "ddns": "plaza-del-sol.ddnsgroup.com",
  "puerto_http": 80,
  "puerto_rtsp": 554
}
```

Solo se utiliza el campo `ddns` para el escaneo.
