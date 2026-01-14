# Ejemplos de Prompts para Testing

Prompts listos para usar con el browser nativo.

## Table of Contents
1. [Formularios](#formularios)
2. [Consola y Errores](#consola-y-errores)
3. [User Flows](#user-flows)
4. [Visual y Responsive](#visual-y-responsive)
5. [Accesibilidad](#accesibilidad)

---

## Formularios

**Validación básica:**
```
Abre localhost:3000/login y verifica que el formulario muestre errores 
cuando se envía vacío. Luego prueba con email inválido.
```

**Test completo de registro:**
```
Abre localhost:3000/register y prueba:
1. Envía vacío - lista errores
2. Datos inválidos (email: "test", password: "123") - verifica errores
3. Datos válidos - verifica registro exitoso
Toma screenshot de cada paso.
```

**Campo específico:**
```
En localhost:3000/contact, prueba el campo teléfono con:
- "abc" (debe rechazar)
- "123" (muy corto)
- "1234567890" (debe aceptar)
```

---

## Consola y Errores

**Revisión general:**
```
Abre localhost:3000 y navega al dashboard. Revisa la consola por 
errores JavaScript o warnings. Lista todos los encontrados.
```

**Debug específico:**
```
Abre localhost:3000/checkout, agrega producto y procede al pago. 
Observa la consola durante todo el proceso y reporta errores.
```

**Network:**
```
Abre localhost:3000/api-test y observa peticiones de red.
Lista llamadas API, status codes y tiempos. Identifica fallidas.
```

---

## User Flows

**Autenticación:**
```
Prueba login/logout en localhost:3000:
1. Verifica no hay sesión
2. Login: test@example.com / testpassword
3. Verifica dashboard
4. Navega a Profile y Settings
5. Logout
6. Verifica no puedes acceder a dashboard
```

**Checkout:**
```
Prueba compra completa en localhost:3000/shop:
1. Busca "Laptop"
2. Agrega al carrito
3. Verifica precio
4. Checkout
5. Llena envío y pago
6. Confirma
7. Verifica confirmación
Screenshots en cada paso.
```

**Wizard:**
```
Prueba onboarding en localhost:3000/onboarding:
1. Completa paso 1, avanza
2. Completa paso 2, regresa
3. Verifica datos del paso 1 persisten
4. Completa todo
5. Intenta acceder directo a /step3 sin completar anteriores
```

---

## Visual y Responsive

**Estilos:**
```
Abre localhost:3000 y verifica header:
- Logo a la izquierda
- Menú a la derecha
- Fondo: #1a1a2e
- Links blancos, hover #4a90d9
Reporta diferencias.
```

**Responsive:**
```
Abre localhost:3000/products y verifica:
1. Desktop (1200px): 4 columnas
2. Tablet (768px): 2 columnas, menú hamburguesa
3. Mobile (375px): 1 columna
Screenshot en cada tamaño.
```

**Regresiones:**
```
Después del deploy, verifica localhost:3000/about:
- Header sin cambios
- Imágenes cargando
- Texto sin truncar
- Botones con estilos correctos
Reporta elementos diferentes o rotos.
```

---

## Accesibilidad

**Navegación por teclado:**
```
En localhost:3000/login:
1. Tab repetidamente - verifica orden de focus
2. Verifica elementos interactivos alcanzables
3. Verifica focus visible
4. Envía formulario solo con teclado (Enter)
```

**ARIA:**
```
Abre localhost:3000 e inspecciona:
- Botones tienen aria-label?
- Links tienen texto descriptivo?
- Formularios tienen labels?
- Imágenes tienen alt?
Lista problemas de accesibilidad.
```
