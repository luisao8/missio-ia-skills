---
name: use-calendar
description: Skill para interactuar con Google Calendar API. Crear, buscar, actualizar y eliminar eventos del calendario.
---

# use-calendar

Skill para gestionar Google Calendar mediante scripts CLI de Python.

## Cuándo usar este skill

Usa este skill cuando el usuario necesite:

- **Ver eventos del día**: Consultar qué hay programado para hoy
- **Buscar eventos**: Encontrar reuniones por nombre, fecha o rango de fechas
- **Crear eventos**: Agendar nuevas reuniones, citas o recordatorios
- **Modificar eventos**: Cambiar hora, título, descripción o asistentes
- **Eliminar eventos**: Cancelar reuniones o eventos
- **Buscar tiempo libre**: Encontrar huecos disponibles para programar algo
- **Listar calendarios**: Ver todos los calendarios disponibles

## Requisitos previos

Las credenciales de Google deben estar configuradas en:
- `MCP_servers/google-credentials/credentials.json` (OAuth client)
- `MCP_servers/google-credentials/calendar_token.pickle` (Token de usuario)

## Scripts disponibles

### get_today.py - Eventos de hoy
```bash
python scripts/get_today.py
```
Retorna JSON array con todos los eventos del día actual.

### search_events.py - Buscar eventos
```bash
python scripts/search_events.py --query "reunión" --start-date "2024-01-15" --end-date "2024-01-20"
```
**Argumentos:**
- `--query`: Texto a buscar en título o descripción
- `--start-date`: Fecha inicio (ISO format, "today", "tomorrow")
- `--end-date`: Fecha fin

### get_event.py - Detalles de un evento
```bash
python scripts/get_event.py --event-id "abc123xyz"
```
**Argumentos:**
- `--event-id`: ID del evento (obtenido de otras consultas)

### create_event.py - Crear evento
```bash
python scripts/create_event.py --title "Reunión de equipo" --date "2024-01-20" --time "10:00" --duration 60
```
**Argumentos:**
- `--title`: Título del evento (requerido)
- `--date`: Fecha del evento (requerido)
- `--time`: Hora de inicio (requerido)
- `--duration`: Duración en minutos (default: 60)
- `--description`: Descripción del evento
- `--location`: Ubicación
- `--attendees`: Lista de emails separados por coma
- `--add-meet`: Agregar enlace de Google Meet

### update_event.py - Actualizar evento
```bash
python scripts/update_event.py --event-id "abc123xyz" --title "Nuevo título" --description "Nueva descripción"
```
**Argumentos:**
- `--event-id`: ID del evento (requerido)
- `--title`: Nuevo título
- `--description`: Nueva descripción
- `--location`: Nueva ubicación
- `--start`: Nueva fecha/hora inicio (ISO format)
- `--end`: Nueva fecha/hora fin (ISO format)
- `--attendees`: Nueva lista de asistentes

### delete_event.py - Eliminar evento
```bash
python scripts/delete_event.py --event-id "abc123xyz"
```
**Argumentos:**
- `--event-id`: ID del evento a eliminar

### find_free_time.py - Buscar tiempo libre
```bash
python scripts/find_free_time.py --duration 30 --start-date "today" --end-date "tomorrow"
```
**Argumentos:**
- `--duration`: Duración mínima en minutos (default: 30)
- `--start-date`: Fecha inicio de búsqueda
- `--end-date`: Fecha fin de búsqueda

### list_calendars.py - Listar calendarios
```bash
python scripts/list_calendars.py
```
Retorna JSON array con id y nombre de cada calendario disponible.

## Formato de respuestas

Todos los scripts retornan JSON válido:

**Éxito:**
```json
{
  "id": "abc123",
  "summary": "Reunión de equipo",
  "start": "2024-01-20T10:00:00+01:00",
  "end": "2024-01-20T11:00:00+01:00"
}
```

**Error:**
```json
{
  "error": "Descripción del error"
}
```

## Timezone

Por defecto se usa `Europe/Madrid`. Para cambiar, configurar la variable de entorno `CALENDAR_TIMEZONE`.
