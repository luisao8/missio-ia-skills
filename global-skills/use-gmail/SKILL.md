---
name: use-gmail
description: Interact with Gmail API to send, search, read, and manage emails
---

# Gmail Skill

Skill para interactuar con Gmail API mediante scripts CLI ejecutables.

## Cuándo Usar

Usa este skill cuando el usuario quiera:
- Enviar emails
- Buscar emails en su bandeja
- Leer emails específicos
- Responder a emails
- Crear borradores
- Gestionar hilos de conversación
- Listar y aplicar etiquetas
- Descargar adjuntos

## Credenciales

Las credenciales de Google OAuth se encuentran en:
- **credentials.json**: `MCP_servers/google-credentials/credentials.json`
- **token**: `MCP_servers/google-credentials/gmail_token.pickle`

Si el token no existe, se iniciará el flujo de autenticación OAuth la primera vez.

## Scripts Disponibles

### send_email.py - Enviar Email

```bash
python scripts/send_email.py --to recipient@example.com --subject "Asunto" --body "Contenido"

# Con CC y BCC
python scripts/send_email.py --to user@example.com --cc other@example.com --bcc hidden@example.com --subject "Meeting" --body "Details here"

# Enviar HTML
python scripts/send_email.py --to user@example.com --subject "Newsletter" --body "<h1>Title</h1><p>Content</p>" --html

# Con adjuntos
python scripts/send_email.py --to user@example.com --subject "Files" --body "See attached" --attachments report.pdf image.png
```

### search_emails.py - Buscar Emails

```bash
# Buscar por remitente
python scripts/search_emails.py --query "from:boss@company.com"

# Emails no leídos
python scripts/search_emails.py --query "is:unread" --max-results 20

# Con adjuntos de la última semana
python scripts/search_emails.py --query "has:attachment newer_than:7d"

# Por etiqueta
python scripts/search_emails.py --label INBOX --query "is:unread"
```

**Query syntax común:**
- `from:email@example.com` - De remitente específico
- `to:email@example.com` - A destinatario específico
- `subject:palabra` - En asunto
- `is:unread` - No leídos
- `is:starred` - Destacados
- `has:attachment` - Con adjuntos
- `after:2024/01/01` - Después de fecha
- `newer_than:7d` - Últimos 7 días
- `"frase exacta"` - Búsqueda exacta

### read_email.py - Leer Email

```bash
# Leer email por ID
python scripts/read_email.py --message-id 18abc123def456
```

Retorna el contenido completo incluyendo body, htmlBody, y lista de adjuntos.

### reply_email.py - Responder Email

```bash
# Responder con texto plano
python scripts/reply_email.py --message-id 18abc123def456 --body "Gracias por tu mensaje!"

# Responder con HTML
python scripts/reply_email.py --message-id 18abc123def456 --body "<p>Gracias!</p>" --html
```

### create_draft.py - Crear Borrador

```bash
# Crear borrador de texto
python scripts/create_draft.py --to user@example.com --subject "Borrador" --body "Contenido del borrador"

# Crear borrador HTML
python scripts/create_draft.py --to user@example.com --subject "Report" --body "<h1>Report</h1>" --html
```

### list_threads.py - Listar Hilos

```bash
# Listar hilos recientes
python scripts/list_threads.py

# Filtrar por query
python scripts/list_threads.py --query "from:team@company.com" --max-results 20
```

### list_labels.py - Listar Etiquetas

```bash
# Ver todas las etiquetas disponibles
python scripts/list_labels.py
```

Retorna ID, nombre y tipo de cada etiqueta.

### add_label.py - Añadir Etiqueta

```bash
# Destacar un mensaje
python scripts/add_label.py --message-id 18abc123def456 --label-id STARRED

# Marcar como importante
python scripts/add_label.py --message-id 18abc123def456 --label-id IMPORTANT

# Añadir etiqueta personalizada
python scripts/add_label.py --message-id 18abc123def456 --label-id Label_123
```

### get_attachments.py - Descargar Adjuntos

```bash
# Descargar adjuntos a carpeta
python scripts/get_attachments.py --message-id 18abc123def456 --output-dir ./downloads
```

## Flujo Típico

1. **Buscar emails**: Usa `search_emails.py` para encontrar emails
2. **Leer detalles**: Usa `read_email.py` con el message ID obtenido
3. **Responder**: Usa `reply_email.py` para responder
4. **Organizar**: Usa `add_label.py` para etiquetar

## Output

Todos los scripts retornan JSON:
- **Éxito**: Objeto o array JSON con los datos
- **Error**: `{"error": "mensaje de error"}`

## Dependencias

Ver `requirements.txt` para las dependencias Python necesarias.
