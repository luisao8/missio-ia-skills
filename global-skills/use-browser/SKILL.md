---
name: use-browser
description: QA y testing de aplicaciones web usando el browser nativo de Claude Code (Claude in Chrome). Usar cuando el usuario mencione "test", "testear", "probar", "QA", "verificar", "browser", "navegador", "debug", "consola", "console", "formulario", "form", "responsive", "visual", o necesite testear una aplicación web, verificar UI, o debuggear errores en el navegador.
---

# Use Browser (Claude in Chrome)

Skill para QA y testing usando el browser nativo de Claude Code. NO usa Playwright.

## Cómo Funciona

El browser nativo de Claude Code permite controlar Chrome directamente desde la terminal:

**Arquitectura:**
- Claude se comunica con Chrome via **Native Messaging API**
- La extensión "Claude in Chrome" recibe comandos y los ejecuta
- Claude abre **nuevos tabs** en TU Chrome (no lanza browser separado)
- **Comparte tus sesiones de login** - si estás logueado en Gmail/LinkedIn/etc, Claude accede

**Qué puede hacer Claude:**
- Navegar a URLs, hacer click, scroll, typing
- Leer la consola, DOM, network requests
- Tomar screenshots y grabar GIFs
- Gestionar tabs (crear, cerrar, cambiar)

**Limitaciones:**
- Requiere Chrome **visible** (no headless, no minimizado)
- No puede resolver CAPTCHAs automáticamente
- No lanza Chrome - debe estar **ya abierto**

## Quick Start

**1. Instalar extensión** (solo una vez):
- Chrome Web Store → "Claude in Chrome" → Instalar

**2. Iniciar Claude con browser:**
```bash
claude --chrome
```

**3. Verificar conexión:**
```
/chrome
```

**4. Habilitar por defecto** (opcional, para no usar --chrome cada vez):
```bash
claude config set browser.enabled true
```
O ejecutar `/chrome` → seleccionar "Enabled by default"

**Requisitos:**
- Extensión "Claude in Chrome" v1.0.36+
- Claude Code v2.0.73+
- Chrome abierto y visible

## Cómo Usar

**Pedir testing directamente:**
```
"Abre localhost:3000 y prueba el formulario de login"
"Verifica que no hay errores en la consola del dashboard"
"Prueba el checkout completo y toma screenshots"
```

**Claude automáticamente:**
1. Abre un nuevo tab en tu Chrome
2. Navega a la URL
3. Ejecuta las acciones (click, typing, etc.)
4. Lee resultados (console, DOM)
5. Reporta lo encontrado

**Comunicación durante bloqueos:**
- CAPTCHA aparece → Claude pausa → "Ya lo resolví, continúa"
- Login requerido → Loguéate manualmente → "Listo"
- Modal bloqueante → Ciérralo → "Cerrado"

## Capacidades

| Categoría | Acciones |
|-----------|----------|
| **Navegación** | Navegar URLs, click, scroll, historial |
| **Interacción** | Typing, formularios, submit, checkboxes, dropdowns |
| **Lectura** | Console logs, DOM, network requests, texto |
| **Captura** | Screenshots, GIFs, full page |
| **Tabs** | Crear, cerrar, cambiar, listar |

## Patrones de QA

### Test de Formularios
```
Abre [URL]/login
1. Envía vacío → verifica errores de validación
2. Datos inválidos → verifica mensajes específicos
3. Datos válidos → verifica submit exitoso
```

### Test de User Flows
```
1. Verificar estado inicial
2. Ejecutar flujo (login, checkout, wizard)
3. Verificar cada paso
4. Verificar estado final
```

### Debug Console
```
Abre [URL] y:
1. Filtra consola por "Error" o "Warning"
2. Lista errores encontrados
3. Identifica peticiones de red fallidas
```

### Test Visual/Responsive
```
1. Desktop (1200px): verificar layout
2. Tablet (768px): verificar adaptación
3. Mobile (375px): verificar columna única
```

**Para patrones detallados:** Ver [references/qa-patterns.md](references/qa-patterns.md)

## Ejemplos de Uso

**Formulario:**
```
Abre localhost:3000/login, intenta enviar vacío y verifica los errores de validación
```

**Debug:**
```
Navega al dashboard y revisa la consola por errores JavaScript
```

**Flow completo:**
```
Prueba el checkout: añade producto, ve al carrito, completa pago, verifica confirmación
```

**Responsive:**
```
Verifica el layout en desktop, tablet y mobile. Toma screenshot en cada tamaño.
```

**Para más ejemplos:** Ver [references/examples.md](references/examples.md)

## Manejo de Bloqueos

| Situación | Acción |
|-----------|--------|
| **CAPTCHA** | Claude pausa. Resuélvelo y di "continúa" |
| **Login wall** | Loguéate manualmente y di "listo" |
| **Modal** | Ciérralo manualmente |
| **Timeout** | Verifica el servidor o recarga |

**Comunicación:** Claude entiende instrucciones naturales: "listo", "continúa", "cerrado", "espera".

## Best Practices

1. **Usar tabs nuevos** - Evita conflictos con tu trabajo
2. **Filtrar console** - Pide patrones específicos, no todo
3. **Aprovechar sesiones** - Si ya estás logueado, Claude accede
4. **Documentar** - Pide screenshots en puntos clave

## Troubleshooting

| Problema | Solución |
|----------|----------|
| Extensión no detectada | Verificar en chrome://extensions, reinstalar |
| Browser no responde | Buscar modals, crear nuevo tab, reiniciar |
| Conexión intermitente | `claude --chrome --debug` para ver logs |

**Para troubleshooting detallado:** Ver [references/troubleshooting.md](references/troubleshooting.md)
