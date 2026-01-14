# Missio IA Skills - Guía de Uso

Colección completa de skills profesionales para Claude Code. Este paquete te permite trabajar con documentos Office, Google Workspace, GitHub, Trello y más, directamente desde Claude.

## 🚀 Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/missio-ia/missio-ia-skills.git
cd missio-ia-skills

# 2. Instalar skills globalmente
cp -r global-skills/* ~/.claude/skills/

# 3. Instalar dependencias según necesites (ver CLAUDE.md)
```

Consulta **CLAUDE.md** para instrucciones detalladas de instalación.

## 📚 Skills Disponibles

### 📄 Office Documents

#### PDF (pdf)
Manipulación completa de documentos PDF con branding de Missio IA.

**Casos de uso:**
- Extraer texto y tablas de PDFs
- Crear PDFs profesionales con logo de Missio IA
- Fusionar y dividir documentos
- Rellenar formularios PDF
- Añadir marcas de agua y protección por contraseña

**Ejemplo:**
```
Claude: "Extrae las tablas del archivo informe.pdf y guárdalas en Excel"
Claude: "Crea un PDF profesional con el logo de Missio IA para este informe"
```

**Ver:** `~/.claude/skills/pdf/SKILL.md` para documentación completa

---

#### Word (docx)
Creación y edición profesional de documentos Word con tracked changes.

**Casos de uso:**
- Crear documentos Word desde cero
- Editar documentos existentes preservando formato
- Trabajar con tracked changes para revisiones
- Convertir markdown a Word
- Extraer contenido de documentos

**Ejemplo:**
```
Claude: "Revisa este contrato y marca los cambios necesarios con tracked changes"
Claude: "Convierte este markdown a un documento Word profesional"
```

**Ver:** `~/.claude/skills/docx/SKILL.md`

---

#### PowerPoint (pptx)
Creación de presentaciones profesionales con diseño creativo.

**Casos de uso:**
- Crear presentaciones desde cero con diseños únicos
- Editar presentaciones existentes
- Usar templates corporativos
- Convertir contenido a slides
- Generar thumbnails de presentaciones

**Ejemplo:**
```
Claude: "Crea una presentación de 10 slides sobre nuestro producto con un diseño moderno"
Claude: "Usa este template y crea slides para mi pitch deck"
```

**Ver:** `~/.claude/skills/pptx/SKILL.md`

---

#### Excel (xlsx)
Creación y análisis de hojas de cálculo con fórmulas y formato profesional.

**Casos de uso:**
- Crear modelos financieros con fórmulas
- Analizar datos con pandas
- Crear dashboards y reportes
- Importar/exportar datos
- Recalcular fórmulas automáticamente

**Ejemplo:**
```
Claude: "Crea un modelo financiero con proyecciones a 5 años"
Claude: "Analiza estos datos de ventas y crea un reporte en Excel"
```

**Ver:** `~/.claude/skills/xlsx/SKILL.md`

---

### 📧 Google Workspace

#### Gmail (use-gmail)
Gestión completa de correo electrónico.

**Casos de uso:**
- Enviar emails con adjuntos
- Buscar y leer emails
- Responder y crear borradores
- Organizar con etiquetas
- Descargar adjuntos

**Ejemplo:**
```
Claude: "Envía un email a luis@missio.ai con el informe adjunto"
Claude: "Busca emails de la última semana que contengan 'proyecto'"
```

**Ver:** `~/.claude/skills/use-gmail/SKILL.md`

---

#### Google Drive (use-drive)
Gestión de archivos en la nube.

**Casos de uso:**
- Subir y descargar archivos
- Crear carpetas y organizar
- Buscar archivos
- Compartir con permisos específicos
- Mover y copiar archivos

**Ejemplo:**
```
Claude: "Sube estos PDFs a mi carpeta de Drive 'Documentos'"
Claude: "Busca todos los archivos de Excel del último mes"
```

**Ver:** `~/.claude/skills/use-drive/SKILL.md`

---

#### Google Docs (use-docs)
Gestión de documentos de Google Docs.

**Casos de uso:**
- Crear documentos con formato
- Editar contenido existente
- Find and replace
- Exportar a PDF/DOCX
- Colaboración en tiempo real

**Ejemplo:**
```
Claude: "Crea un Google Doc con las notas de la reunión"
Claude: "Reemplaza 'Cliente A' por 'Acme Corp' en todo el documento"
```

**Ver:** `~/.claude/skills/use-docs/SKILL.md`

---

#### Google Calendar (use-calendar)
Gestión de calendario y eventos.

**Casos de uso:**
- Ver agenda del día
- Crear reuniones con invitados
- Buscar tiempo libre
- Añadir Google Meet a eventos
- Modificar y cancelar eventos

**Ejemplo:**
```
Claude: "¿Qué tengo programado para hoy?"
Claude: "Agenda una reunión con el equipo mañana a las 10am con Meet link"
```

**Ver:** `~/.claude/skills/use-calendar/SKILL.md`

---

#### Google Meet (use-meet)
Gestión de videollamadas.

**Casos de uso:**
- Crear espacios de reunión
- Generar links de Meet
- Finalizar reuniones remotamente
- Acceder a grabaciones
- Obtener transcripciones

**Ejemplo:**
```
Claude: "Crea un Meet para la reunión de equipo"
Claude: "Dame la transcripción de la última reunión"
```

**Ver:** `~/.claude/skills/use-meet/SKILL.md`

---

### 🔧 Development Tools

#### GitHub (use-github)
Gestión de repositorios, issues y pull requests.

**Casos de uso:**
- Listar y buscar repositorios
- Crear y gestionar issues
- Crear y mergear PRs
- Buscar en código
- Gestionar branches

**Ejemplo:**
```
Claude: "Lista los issues abiertos del repo missio-ia/app"
Claude: "Crea un PR de la branch feature/auth a main"
```

**Ver:** `~/.claude/skills/use-github/SKILL.md`

---

#### Browser Testing (use-browser)
QA y testing de aplicaciones web.

**Casos de uso:**
- Probar formularios y validaciones
- Verificar errores de consola
- Testing responsive
- Capturar screenshots
- Debug de aplicaciones web

**Ejemplo:**
```
Claude: "Abre localhost:3000 y prueba el formulario de login"
Claude: "Verifica que no hay errores en la consola del dashboard"
```

**Ver:** `~/.claude/skills/use-browser/SKILL.md`

**Nota:** Requiere Chrome abierto y extensión "Claude in Chrome"

---

### 📋 Project Management

#### Trello (use-trello)
Gestión de tableros y tareas.

**Casos de uso:**
- Listar boards y cards
- Crear tareas
- Mover cards entre listas
- Añadir comentarios y etiquetas
- Archivar cards

**Ejemplo:**
```
Claude: "Crea una card en mi board de 'Proyectos' llamada 'Nueva feature'"
Claude: "Mueve la card de 'Login fix' a la lista 'Done'"
```

**Ver:** `~/.claude/skills/use-trello/SKILL.md`

---

## 🎯 Casos de Uso Comunes

### Workflow de Reportes

```
1. Claude: "Analiza estos datos de ventas" (xlsx skill)
2. Claude: "Crea un PDF con el análisis y gráficos" (pdf skill)
3. Claude: "Sube el PDF a Drive en la carpeta 'Reportes'" (use-drive)
4. Claude: "Envía el reporte por email al equipo ejecutivo" (use-gmail)
```

### Workflow de Presentaciones

```
1. Claude: "Crea una presentación de 15 slides sobre Q1 results" (pptx skill)
2. Claude: "Añade los datos de esta tabla de Excel" (xlsx skill)
3. Claude: "Sube la presentación a Drive" (use-drive)
4. Claude: "Crea un evento de calendar para presentarla" (use-calendar)
```

### Workflow de Desarrollo

```
1. Claude: "Lista los issues abiertos del proyecto" (use-github)
2. Claude: "Testea la nueva feature en localhost:3000" (use-browser)
3. Claude: "Crea un PR con los cambios" (use-github)
4. Claude: "Mueve la tarjeta de Trello a 'Code Review'" (use-trello)
```

### Workflow de Documentación

```
1. Claude: "Crea un Google Doc con las especificaciones" (use-docs)
2. Claude: "Genera un PDF del doc para archivo" (use-docs export)
3. Claude: "Crea un Word para enviar al cliente" (docx skill)
4. Claude: "Sube ambos archivos a Drive" (use-drive)
```

## 🔐 Configuración de Credenciales

### Google Workspace Skills

Todos los skills de Google (gmail, drive, docs, calendar, meet) comparten las mismas credenciales:

1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilitar las APIs necesarias
3. Crear credenciales OAuth 2.0
4. Descargar y guardar en: `~/MCP_servers/google-credentials/credentials.json`

**Ubicación de tokens:**
- Gmail: `~/MCP_servers/google-credentials/gmail_token.pickle`
- Drive: `~/MCP_servers/google-credentials/token-drive.json`
- Calendar: `~/MCP_servers/google-credentials/calendar_token.pickle`
- Meet: `~/MCP_servers/google-credentials/token_meet.pickle`

### GitHub

```bash
# Obtener token personal: https://github.com/settings/tokens
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
```

### Trello

```bash
# Obtener credenciales: https://trello.com/app-key
export TRELLO_API_KEY="your_key"
export TRELLO_TOKEN="your_token"
```

## 📖 Documentación por Skill

Cada skill incluye su propio archivo `SKILL.md` con:
- Descripción detallada
- Instrucciones de instalación
- Ejemplos de uso
- Referencia de comandos/scripts
- Troubleshooting

## 🤝 Contribuir

¿Tienes ideas para nuevos skills o mejoras?
1. Fork el repositorio
2. Crea una branch con tu feature
3. Añade tests si aplica
4. Envía un Pull Request

## 📝 Licencia

Los skills incluidos tienen diferentes licencias:
- Skills de Office (pdf, docx, pptx, xlsx): Propietario - Ver LICENSE.txt en cada skill
- Skills de APIs: Verificar licencia individual

## 🐛 Reportar Issues

Si encuentras problemas:
1. Verifica que tienes las dependencias instaladas
2. Revisa el archivo SKILL.md del skill específico
3. Abre un issue en GitHub con:
   - Descripción del problema
   - Skill afectado
   - Pasos para reproducir
   - Logs de error (si aplica)

---

**Desarrollado por Missio IA** 🚀
