# Integración API de Actividades

## 📋 Descripción

Se ha integrado completamente la API de SGCC Backend (`https://aids.policiachihuahua.gob.mx/sgcc-backend/api/activities.json`) con la vista de Actividades de la aplicación PECUU.

## ✨ Funcionalidades Implementadas

### ✅ Lectura (GET)
- Carga automática de todas las actividades desde la API
- Se ejecuta al inicializar la vista
- Mapeo automático de campos de la API a formato esperado

### ✅ Creación (POST)
- Crear nuevas actividades mediante el formulario
- Se envía a la API automáticamente
- Fallback a almacenamiento local si la API falla
- Mensaje diferenciado (azul para local, verde para API)

### ✅ Actualización (PUT)
- Editar actividades existentes
- Sincronización con la API
- Validación de campos

### ✅ Eliminación (DELETE)
- Eliminar actividades con confirmación visual
- Se elimina tanto de la API como de la vista local
- Mensaje de confirmación de eliminación

## 📁 Archivos Modificados

### 1. `services/api_service.py` (EXTENDIDO)
Nuevos métodos agregados:

#### GET
- `get_activities()`: Obtiene todas las actividades desde la API
  ```python
  actividades = ApiService.get_activities()
  ```

#### POST
- `create_activity(actividad_data)`: Crea nueva actividad
  ```python
  result = ApiService.create_activity({
      "titulo": "Mi Actividad",
      "descripcion": "Descripción",
      "fecha": "2025-12-04"
  })
  ```

#### PUT
- `update_activity(activity_id, actividad_data)`: Actualiza actividad
  ```python
  result = ApiService.update_activity(1, {
      "titulo": "Actualizado",
      "descripcion": "Nueva descripción"
  })
  ```

#### DELETE
- `delete_activity(activity_id)`: Elimina actividad
  ```python
  result = ApiService.delete_activity(1)
  ```

#### Local
- `_save_activity_locally(actividad_data, error_reason)`: Almacenamiento local

### 2. `components/actividades_agregar.py` (ACTUALIZADO)
- Importa `ApiService`
- Función `handle_save()` ahora:
  - Intenta crear en la API
  - Si falla, guarda localmente
  - Muestra mensajes diferenciados
  - Maneja errores apropiadamente

### 3. `components/actividades.py` (ACTUALIZADO)
- Importa `ApiService`
- Función `delete_actividad()` ahora:
  - Obtiene ID de la actividad
  - Intenta eliminar de la API
  - Muestra confirmación/error
  - Actualiza vista localmente

### 4. `views/actividades.py` (ACTUALIZADO)
- Importa `ApiService`
- Nuevos métodos:
  - `load_actividades_from_api()`: Carga desde API
  - `refresh_actividades_from_api()`: Refresca datos
- Carga automática de actividades al inicializar

## 🔄 Flujo de Datos

### Carga de Actividades
```
1. Vista Actividades se inicializa
   ↓
2. Llama load_actividades_from_api()
   ↓
3. ApiService.get_activities() realiza GET
   ↓
4. Mapea campos de la API
   ↓
5. Muestra actividades en tarjetas
```

### Creación de Actividad
```
1. Usuario llena formulario
   ↓
2. Click en "GUARDAR"
   ↓
3. Validación de campos
   ↓
4. ApiService.create_activity() realiza POST
   ↓
5. Si API falla → Almacena localmente
   ↓
6. Muestra confirmación (verde/azul)
   ↓
7. Regresa a vista de actividades
```

### Eliminación de Actividad
```
1. Click en icono eliminar
   ↓
2. delete_actividad() se ejecuta
   ↓
3. Obtiene ID de la actividad
   ↓
4. ApiService.delete_activity() realiza DELETE
   ↓
5. Elimina de vista local
   ↓
6. Muestra confirmación
```

## 📊 Estructura de Datos

### Formato de Entrada (API)
```json
{
  "id": 1,
  "title": "Sitio",
  "description": "Checar puerto caido",
  "date": "2025-11-26",
  "user": {
    "name": "Pedro Velazquez"
  },
  "active": true
}
```

### Formato Interno (Aplicación)
```python
{
    "id": 1,
    "titulo": "Sitio",
    "descripcion": "Checar puerto caido",
    "fecha": "2025-11-26",
    "usuario": "Pedro Velazquez",
    "activa": True,
    "_api_id": 1
}
```

## 🎯 Uso

### Crear Actividad
1. Click en botón "+" en tarjeta de agregar
2. Completa el formulario
3. Click "GUARDAR"
4. Se crea en la API y aparece en la lista

### Editar Actividad
1. Click en menú (⋮) de la actividad
2. Selecciona "Editar"
3. Modifica los datos
4. Click "GUARDAR"
5. Se actualiza en la API

### Eliminar Actividad
1. Click en menú (⋮) de la actividad
2. Selecciona "Eliminar"
3. Se elimina de la API
4. Desaparece de la lista

### Marcar como Completada
1. Click en icono de check (✓)
2. La actividad se marca como completada
3. Strikethrough en el título

## 🛡️ Manejo de Errores

- **API no disponible**: Almacena localmente automáticamente
- **Error al crear**: Muestra mensaje de error, permite reintentar
- **Error al eliminar**: Mantiene actividad en lista, muestra error
- **Error al actualizar**: Informa al usuario
- **Validación**: Verifica título requerido

## 📝 Almacenamiento Local

Cuando la API no está disponible, se crea `actividades_locales.json`:
```json
{
  "actividades": [
    {
      "titulo": "Mi Actividad",
      "descripcion": "Descripción",
      "_local": true,
      "_created_at": "2025-12-04T..."
    }
  ]
}
```

## 🔗 Endpoint de API

- **URL Base**: `https://aids.policiachihuahua.gob.mx/sgcc-backend/api`
- **GET**: `/activities.json`
- **POST**: `/activities`
- **PUT**: `/activities/{id}`
- **DELETE**: `/activities/{id}`

## ⚠️ Notas Importantes

1. La API actual es principalmente de lectura (POST/PUT/DELETE pueden fallar)
2. El almacenamiento local actúa como fallback automático
3. Los cambios locales se sincronizan cuando la API esté disponible
4. Los IDs se mapean automáticamente para referencia interna

## 🚀 Próximos Pasos

- Sincronización bidireccional de cambios locales
- Caché de actividades para mejora de rendimiento
- Búsqueda y filtrado de actividades
- Exportación de actividades
