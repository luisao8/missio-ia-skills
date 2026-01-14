# QA Patterns

Patrones detallados para testing con el browser nativo.

## Table of Contents
1. [Test de Formularios](#test-de-formularios)
2. [Test de User Flows](#test-de-user-flows)
3. [Test Visual](#test-visual)
4. [Debug](#debug)

---

## Test de Formularios

### Estructura del test
```
1. Abrir la página con el formulario
2. Probar validación con datos inválidos
3. Verificar mensajes de error
4. Probar con datos válidos
5. Verificar submit exitoso
```

### Ejemplo: Formulario de Login
```
Abre [URL]/login

PASO 1 - Campos vacíos:
- Click en 'Submit' sin llenar nada
- Verifica "Email es requerido"
- Verifica "Password es requerido"

PASO 2 - Formato inválido:
- Email: "invalido", Password: "123"
- Verifica "Email no válido"
- Verifica "Password mínimo 8 caracteres"

PASO 3 - Credenciales incorrectas:
- Email válido, password incorrecto
- Verifica "Credenciales inválidas"

PASO 4 - Login exitoso:
- Credenciales correctas
- Verifica redirección a dashboard
```

### Checklist de validaciones

| Campo | Validaciones |
|-------|-------------|
| Email | Vacío, formato, dominio, duplicado |
| Password | Vacío, longitud, mayúsculas, números, especiales |
| Teléfono | Vacío, letras, formato, longitud |
| Fecha | Vacío, formato, rango |
| Número | Vacío, letras, negativo, rango |

---

## Test de User Flows

### Login/Logout Flow
```
1. INICIO: Verificar no hay sesión (botón "Login" visible)
2. LOGIN: Credenciales → dashboard → nombre de usuario visible
3. NAVEGACIÓN: Acceder a páginas protegidas
4. LOGOUT: Click logout → redirección → sin sesión
5. VERIFICACIÓN: Intentar acceder a /dashboard → redirección a login
```

### Checkout Flow
```
1. BROWSE: Buscar producto → ver detalle
2. CARRITO: Agregar → verificar contador
3. CHECKOUT: Verificar productos → llenar envío
4. PAGO: Seleccionar método → verificar total
5. CONFIRMACIÓN: Número de orden → carrito vacío
```

### Wizard Multi-paso
```
1. Paso 1: Llenar → siguiente
2. Paso 2: Llenar → atrás → verificar datos persisten
3. Completar todos los pasos
4. Intentar saltar pasos (modificar URL) → verificar protección
```

---

## Test Visual

### Comparar con Mockups
```
1. LAYOUT: Posición de header, hero, cards, footer
2. ESTILOS: Colores (#hex), tipografía, espaciado
3. COMPONENTES: Botones, links, forms, cards (hover states)
```

### Test Responsive
```
DESKTOP (1920x1080): Layout completo, menú horizontal
TABLET (768x1024): 2 columnas, menú hamburguesa
MOBILE (375x667): 1 columna, todo legible, botones tocables (44px min)
```

### Detectar Regresiones
```
Checklist post-deploy:
[ ] Elementos alineados
[ ] Texto sin truncar
[ ] Imágenes correctas
[ ] Colores correctos
[ ] Espaciado consistente
[ ] Sin scroll horizontal
```

---

## Debug

### Console Errors
```
1. Abrir página
2. Filtrar por tipo: Error (rojo), Warning (amarillo)
3. Interactuar y observar nuevos errores
4. Documentar: acción → error
```

**Errores comunes:**
- "Cannot read property X of undefined" → objeto null
- "X is not a function" → función no definida
- "Failed to fetch" → error de red
- "CORS error" → cross-origin

### Network Requests
```
1. Listar peticiones
2. Filtrar: XHR/Fetch (APIs), JS, CSS, Img
3. Verificar status codes: 200 OK, 4xx error cliente, 5xx error servidor
4. Identificar: lentas (>1s), fallidas, duplicadas
```

### Inspeccionar DOM
```
- "Inspecciona el botón 'Submit'" → ver HTML
- "Qué color tiene el botón?" → estilos computados
- "El input está dentro del form?" → jerarquía
```
