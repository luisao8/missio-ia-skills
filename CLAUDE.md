# Missio IA Skills Package

Este paquete contiene una colección de skills profesionales para Claude Code, diseñados para trabajar con documentos Office, Google Workspace, GitHub, Trello y más.

## Instalación

### Requisitos Previos

- **Claude Code** instalado y configurado
- **Python 3.11+** para los skills que usan APIs
- **Node.js 18+** para skills que requieren npm packages

### Instalación de Skills Globales

Los skills en este paquete están diseñados para ser instalados **globalmente** en tu configuración de Claude Code, lo que significa que estarán disponibles en todos tus proyectos.

#### Opción 1: Copiar manualmente

```bash
# Copiar todos los skills al directorio global de Claude
cp -r global-skills/* ~/.claude/skills/
```

#### Opción 2: Symlink (recomendado para desarrollo)

```bash
# Crear symlinks para mantener los skills actualizados
cd ~/.claude/skills/
ln -s /ruta/completa/a/missio-ia-skills/global-skills/* .
```

### Instalación de Dependencias

Cada skill tiene sus propias dependencias. Instálalas según necesites:

#### Skills de Office (pdf, docx, pptx, xlsx)

```bash
# Instalar dependencias Python
pip install -r ~/.claude/skills/pdf/requirements.txt
pip install -r ~/.claude/skills/docx/requirements.txt
pip install -r ~/.claude/skills/pptx/requirements.txt
pip install -r ~/.claude/skills/xlsx/requirements.txt

# Instalar dependencias npm (para pptx)
npm install -g pptxgenjs playwright sharp
```

#### Skills de Google Workspace (gmail, drive, docs, calendar, meet)

```bash
# Instalar dependencias Python
pip install -r ~/.claude/skills/use-gmail/requirements.txt
pip install -r ~/.claude/skills/use-drive/requirements.txt
pip install -r ~/.claude/skills/use-docs/requirements.txt
pip install -r ~/.claude/skills/use-calendar/requirements.txt
pip install -r ~/.claude/skills/use-meet/requirements.txt
```

**Configurar credenciales de Google:**
1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilitar las APIs necesarias (Gmail, Drive, Docs, Calendar, Meet)
3. Crear credenciales OAuth 2.0
4. Descargar `credentials.json` y colocar en `~/MCP_servers/google-credentials/`

#### Skill de GitHub

```bash
# Instalar dependencias Python
pip install -r ~/.claude/skills/use-github/requirements.txt

# Configurar token de GitHub
export GITHUB_TOKEN="tu_token_aqui"
# O añadir a ~/.bashrc o ~/.zshrc para hacerlo permanente
```

Obtener token: https://github.com/settings/tokens

#### Skill de Trello

```bash
# Instalar dependencias Python
pip install -r ~/.claude/skills/use-trello/requirements.txt

# Configurar API key y token de Trello
export TRELLO_API_KEY="tu_api_key"
export TRELLO_TOKEN="tu_token"
# O añadir a ~/.bashrc o ~/.zshrc para hacerlo permanente
```

Obtener credenciales: https://trello.com/app-key

#### Skill de Browser (use-browser)

**Requisitos especiales:**
1. Instalar extensión "Claude in Chrome" desde Chrome Web Store
2. Tener Chrome abierto y visible (no minimizado)
3. Iniciar Claude con: `claude --chrome`

Para habilitar por defecto:
```bash
claude config set browser.enabled true
```

## Verificación de Instalación

Para verificar que los skills están instalados correctamente:

```bash
# Listar skills instalados
ls -la ~/.claude/skills/

# Verificar que Claude reconoce los skills
# Inicia Claude y escribe /
# Deberías ver los skills disponibles en el autocompletado
```

## Estructura del Paquete

```
missio-ia-skills/
├── CLAUDE.md                    # Este archivo
├── README.md                    # Documentación de uso
└── global-skills/               # Skills globales
    ├── pdf/                     # Manipulación de PDFs
    ├── docx/                    # Documentos Word
    ├── pptx/                    # Presentaciones PowerPoint
    ├── xlsx/                    # Hojas de cálculo Excel
    ├── use-gmail/               # Gmail API
    ├── use-drive/               # Google Drive API
    ├── use-docs/                # Google Docs API
    ├── use-calendar/            # Google Calendar API
    ├── use-meet/                # Google Meet API
    ├── use-github/              # GitHub API
    ├── use-trello/              # Trello API
    ├── use-browser/             # Testing con Chrome
    └── requirements.txt         # Dependencias compartidas
```

## Clasificación de Skills

### Skills Globales vs Locales

**Todos los skills en este paquete son GLOBALES**, lo que significa:
- Se instalan en `~/.claude/skills/` (no en `.claude/skills/` del proyecto)
- Están disponibles en todos tus proyectos de Claude Code
- Son herramientas de propósito general que no dependen de un proyecto específico

**Cuándo usar skills globales:**
- Herramientas que usas frecuentemente en múltiples proyectos
- Integraciones con servicios externos (Gmail, GitHub, Trello)
- Utilidades de procesamiento de documentos (PDF, Word, Excel, PowerPoint)

**Cuándo crear skills locales** (para otros proyectos):
- Lógica específica de tu proyecto o dominio
- Configuraciones únicas de tu empresa
- Scripts que dependen de la estructura de tu proyecto

## Actualización

Para actualizar los skills:

```bash
# Si usaste symlinks (recomendado)
cd missio-ia-skills
git pull origin main

# Si copiaste manualmente
cd missio-ia-skills
git pull origin main
cp -r global-skills/* ~/.claude/skills/
```

## Soporte y Contribuciones

- **Issues:** Reporta problemas en el repositorio de GitHub
- **Pull Requests:** Contribuciones bienvenidas
- **Documentación:** Cada skill tiene su propio SKILL.md con instrucciones detalladas

## Licencia

Ver LICENSE.txt en cada skill individual. Algunos skills son propietarios de Missio IA.
