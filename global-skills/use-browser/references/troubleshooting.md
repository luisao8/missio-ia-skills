# Troubleshooting

Soluciones a problemas comunes con el browser nativo.

## Table of Contents
1. [Extensión No Detectada](#extensión-no-detectada)
2. [Browser No Responde](#browser-no-responde)
3. [Errores de Instalación](#errores-de-instalación)
4. [Problemas de Conexión](#problemas-de-conexión)
5. [Comandos de Diagnóstico](#comandos-de-diagnóstico)

---

## Extensión No Detectada

**Síntomas:** `/chrome` muestra "Extension not connected"

**Soluciones:**

1. **Verificar instalación:**
   - Abrir `chrome://extensions`
   - Buscar "Claude in Chrome"
   - Verificar switch azul (habilitada)

2. **Reinstalar:**
   - Desinstalar extensión
   - Chrome Web Store → instalar "Claude in Chrome"

3. **Verificar Native Messaging:**
   ```bash
   claude --chrome --debug
   ```

4. **Reiniciar Chrome:**
   - Cerrar completamente (verificar en Activity Monitor)
   - Abrir Chrome
   - Ejecutar `claude --chrome`

---

## Browser No Responde

**Síntomas:** Comandos sin efecto, timeouts

**Soluciones:**

1. **Chrome visible:** No minimizado, ventana activa

2. **Tab correcto:** El tab objetivo debe estar enfocado

3. **Recargar extensión:**
   - `chrome://extensions`
   - Click en icono reload de la extensión

4. **Recursos:** Cerrar tabs innecesarios, reiniciar Chrome

---

## Errores de Instalación

### Native Messaging Host no configurado
```
Error: "Failed to connect to native messaging host"
```

**Verificar archivo existe en:**
- macOS: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`
- Linux: `~/.config/google-chrome/NativeMessagingHosts/`
- Windows: `HKEY_CURRENT_USER\Software\Google\Chrome\NativeMessagingHosts`

### Permisos insuficientes
```
Error: "Permission denied"
```

**Solución:**
```bash
chmod +x /path/to/native-messaging-host
```

### Versión incompatible
```
Error: "Incompatible extension version"
```

**Solución:**
- Actualizar Claude CLI: `claude update`
- Actualizar extensión en Chrome Web Store

---

## Problemas de Conexión

**Síntomas:** Conexión intermitente

**Soluciones:**

1. **Ver logs:**
   ```bash
   claude --chrome --debug 2>&1 | tee chrome-debug.log
   ```

2. **Verificar firewalls:** Native Messaging usa comunicación local

3. **Reinicio completo:**
   ```bash
   # 1. Cerrar Claude
   # 2. Cerrar Chrome completamente
   # 3. Esperar 5 segundos
   # 4. Abrir Chrome
   # 5. claude --chrome
   ```

---

## Comandos de Diagnóstico

```bash
# Estado de conexión
/chrome

# Versión de extensión
/chrome version

# Test básico
/chrome ping

# Debug en tiempo real
claude --chrome --debug

# Versiones
claude --version
# Chrome: chrome://version
```

---

## Contactar Soporte

**Información a recopilar:**
- `claude --version`
- Versión de Chrome (`chrome://version`)
- Versión de extensión
- Sistema operativo
- Logs de debug

**Recursos:**
- GitHub Issues del proyecto
- Documentación actualizada
