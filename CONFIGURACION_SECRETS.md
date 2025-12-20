# 🔐 Guía Paso a Paso: Configurar Variables de Entorno (GitHub Secrets)

## 📋 Resumen Rápido

Necesitas configurar **3 Secrets** en GitHub para que el bot funcione:
1. `RAPIDAPI_KEY` - Tu API key de JSearch
2. `TELEGRAM_BOT_TOKEN` - Token de tu bot de Telegram
3. `TELEGRAM_CHAT_ID` - Tu Chat ID de Telegram

---

## 🎯 PASO 1: Obtener RAPIDAPI_KEY

### 1.1 Ir a RapidAPI

Ve a: **https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch**

### 1.2 Registrarte o Iniciar Sesión

- Si no tienes cuenta: Click en **"Sign Up"** (esquina superior derecha)
- Si ya tienes cuenta: Click en **"Log In"**

### 1.3 Suscribirte al API (Gratis)

1. Una vez en la página de JSearch API
2. Click en el botón **"Subscribe to Test"**
3. Selecciona el plan **"BASIC"** (FREE)
   - ✅ 100 requests/mes
   - ✅ $0.00/mes
4. Click en **"Subscribe"**

### 1.4 Copiar tu API Key

1. Después de suscribirte, verás la página de "Endpoints"
2. En el lado derecho verás **"Header Parameters"**
3. Busca **"X-RapidAPI-Key"**
4. Copia el valor que aparece (algo como: `a1b2c3d4e5f6g7h8...`)

**⚠️ IMPORTANTE:** Guarda esta key en un lugar seguro, la necesitarás en el Paso 4

```
Ejemplo de API Key:
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

---

## 🤖 PASO 2: Crear Bot de Telegram

### 2.1 Abrir Telegram

Abre la aplicación de Telegram en tu teléfono o computadora

### 2.2 Buscar BotFather

1. En la barra de búsqueda, escribe: **@BotFather**
2. Click en el contacto oficial (tiene una marca de verificación ✓)

### 2.3 Crear el Bot

1. Envía el comando: `/newbot`
2. BotFather te preguntará el nombre del bot:
   - Ejemplo: `PulseBot Job Search`
3. Luego te pedirá un username (debe terminar en '_bot'):
   - Ejemplo: `pulsebot_empleos_bot`
4. BotFather te enviará un mensaje con el **token**

### 2.4 Copiar el Token

El mensaje de BotFather se verá así:

```
Done! Congratulations on your new bot.
You will find it at t.me/pulsebot_empleos_bot

Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz-ABCDEFG

For a description of the Bot API, see this page:
https://core.telegram.org/bots/api
```

**Copia el token** (la línea larga de números y letras)

**⚠️ IMPORTANTE:** Guarda este token, lo necesitarás en el Paso 4

```
Ejemplo de Token:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz-ABCDEFG
```

---

## 📱 PASO 3: Obtener Chat ID de Telegram

### 3.1 Enviar Mensaje al Bot

1. Busca tu bot en Telegram (el que acabas de crear)
2. Envíale cualquier mensaje, por ejemplo: `Hola`

### 3.2 Obtener el Chat ID

#### Método A: Usando el navegador

1. Abre tu navegador web
2. En la barra de direcciones, escribe:
   ```
   https://api.telegram.org/bot<TU_TOKEN>/getUpdates
   ```
   **⚠️ Reemplaza `<TU_TOKEN>` con tu token real** (el del Paso 2.4)

3. Presiona Enter
4. Verás un JSON con información
5. Busca la sección `"chat"`:
   ```json
   {
     "update_id": 123456789,
     "message": {
       "message_id": 1,
       "from": { ... },
       "chat": {
         "id": 987654321,  ← ESTE ES TU CHAT ID
         "first_name": "Tu Nombre",
         "type": "private"
       },
       "text": "Hola"
     }
   }
   ```

6. **Copia el número** que aparece en `"id"` dentro de `"chat"`

**⚠️ IMPORTANTE:** Guarda este número, lo necesitarás en el Paso 4

```
Ejemplo de Chat ID:
987654321
```

#### Método B: Usando un bot helper (alternativo)

1. Busca en Telegram: **@userinfobot**
2. Envíale el comando: `/start`
3. El bot te responderá con tu Chat ID

### 3.3 Para Canal o Grupo (opcional)

Si quieres que el bot envíe mensajes a un canal o grupo:

1. Crea el canal/grupo
2. Añade tu bot como administrador
3. Envía un mensaje en el canal/grupo
4. Usa el método del navegador (Paso 3.2)
5. El Chat ID será **negativo** (ej: `-1001234567890`)

---

## ⚙️ PASO 4: Configurar GitHub Secrets

Ahora que tienes las 3 credenciales, vamos a configurarlas en GitHub.

### 4.1 Ir a tu Repositorio

Abre tu navegador y ve a:
```
https://github.com/marcelodanieldm/PulseBot
```

### 4.2 Ir a Settings

1. En tu repositorio, click en **"Settings"** (última opción del menú superior)
2. Si no ves "Settings", asegúrate de estar logueado y ser el dueño del repositorio

### 4.3 Ir a Secrets and Variables

1. En el menú lateral izquierdo, busca **"Secrets and variables"**
2. Click en **"Secrets and variables"**
3. Click en **"Actions"**

### 4.4 Añadir el Primer Secret (RAPIDAPI_KEY)

1. Click en el botón verde **"New repository secret"**
2. En el campo **"Name"**, escribe exactamente:
   ```
   RAPIDAPI_KEY
   ```
   ⚠️ **Todo en MAYÚSCULAS, sin espacios**

3. En el campo **"Secret"**, pega tu API key de RapidAPI (del Paso 1.4)
4. Click en **"Add secret"**

### 4.5 Añadir el Segundo Secret (TELEGRAM_BOT_TOKEN)

1. Click nuevamente en **"New repository secret"**
2. En el campo **"Name"**, escribe exactamente:
   ```
   TELEGRAM_BOT_TOKEN
   ```
   ⚠️ **Todo en MAYÚSCULAS, sin espacios**

3. En el campo **"Secret"**, pega tu token de Telegram (del Paso 2.4)
4. Click en **"Add secret"**

### 4.6 Añadir el Tercer Secret (TELEGRAM_CHAT_ID)

1. Click nuevamente en **"New repository secret"**
2. En el campo **"Name"**, escribe exactamente:
   ```
   TELEGRAM_CHAT_ID
   ```
   ⚠️ **Todo en MAYÚSCULAS, sin espacios**

3. En el campo **"Secret"**, pega tu Chat ID de Telegram (del Paso 3.2)
4. Click en **"Add secret"**

### 4.7 Verificar

Deberías ver 3 secrets en la lista:
- ✅ RAPIDAPI_KEY
- ✅ TELEGRAM_BOT_TOKEN
- ✅ TELEGRAM_CHAT_ID

**¡Importante!** No podrás ver el valor de los secrets después de guardarlos (es por seguridad)

---

## ✅ PASO 5: Probar el Bot

### 5.1 Ejecutar Manualmente

1. Ve a la pestaña **"Actions"** en tu repositorio
   ```
   https://github.com/marcelodanieldm/PulseBot/actions
   ```

2. En el lado izquierdo, click en **"PulseBot Job Search"**

3. En el lado derecho, click en el botón **"Run workflow"**

4. Verás un dropdown, selecciona la rama **"main"**

5. Click en el botón verde **"Run workflow"**

### 5.2 Ver el Progreso

1. Espera unos segundos y verás aparecer un nuevo workflow en la lista
2. Click en él para ver el progreso en tiempo real
3. Click en **"search-jobs"** para ver los logs detallados

### 5.3 Verificar Logs

Deberías ver algo como:
```
🤖 PulseBot - Buscador de Empleos
==================================================
📋 Criterios de búsqueda:
  - Puesto: Software Engineer
  - Ubicación: Latin America
  ...
📂 Cargando historial de ofertas enviadas...
✅ Historial cargado: 0 ofertas previamente enviadas

🔍 Buscando página 1...
✅ Encontrados 10 trabajos en página 1
...
```

### 5.4 Verificar en Telegram

1. Abre Telegram
2. Ve a tu chat con el bot
3. Deberías ver mensajes con ofertas de empleo
4. Cada mensaje incluye:
   - Título del puesto
   - Empresa
   - Ubicación
   - Salario (si disponible)
   - Análisis de reputación
   - Link de aplicación

---

## 🔄 PASO 6: Ejecución Automática

Una vez configurado, el bot se ejecutará automáticamente:

### Horarios (UTC):
- **00:00 UTC** (9:00 PM hora Este, día anterior)
- **06:00 UTC** (3:00 AM hora Este)
- **12:00 UTC** (9:00 AM hora Este)
- **18:00 UTC** (3:00 PM hora Este)

### ¿Qué pasará?
- ✅ El bot buscará ofertas nuevas
- ✅ Filtrará duplicados automáticamente
- ✅ Enviará solo ofertas nuevas a Telegram
- ✅ Actualizará el historial en GitHub

---

## 🐛 Solución de Problemas

### ❌ Error: "RAPIDAPI_KEY no configurada"

**Causa:** El secret no está configurado o el nombre es incorrecto

**Solución:**
1. Ve a Settings → Secrets and variables → Actions
2. Verifica que el secret se llame exactamente: `RAPIDAPI_KEY` (mayúsculas)
3. Si está mal escrito, bórralo y créalo nuevamente

### ❌ Error: "Credenciales de Telegram no configuradas"

**Causa:** Los secrets de Telegram no están configurados

**Solución:**
1. Verifica que ambos secrets existan:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
2. Los nombres deben ser exactos (mayúsculas)

### ❌ No se reciben mensajes en Telegram

**Causas posibles:**

1. **Chat ID incorrecto**
   - Solución: Obtén el Chat ID nuevamente (Paso 3)
   - Recuerda: puede ser negativo para grupos/canales

2. **Bot bloqueado**
   - Solución: Desbloquea el bot en Telegram

3. **Token incorrecto**
   - Solución: Genera un nuevo token con @BotFather usando `/newbot`

### ❌ No se encuentran trabajos

**Es normal si:**
- ✅ Todos ya fueron enviados (sistema anti-duplicados)
- ✅ No hay ofertas nuevas para esos criterios
- ✅ La API no tiene resultados

**Verifica en los logs:**
- Busca: "No hay nuevas ofertas"
- Esto significa que el sistema está funcionando

---

## 📊 Resumen de URLs Importantes

### Para configurar:
- **RapidAPI JSearch:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- **Telegram BotFather:** https://t.me/botfather
- **GitHub Secrets:** https://github.com/marcelodanieldm/PulseBot/settings/secrets/actions

### Para monitorear:
- **GitHub Actions:** https://github.com/marcelodanieldm/PulseBot/actions
- **Repositorio:** https://github.com/marcelodanieldm/PulseBot

---

## 📝 Checklist Final

Marca cada item cuando lo completes:

- [ ] ✅ Obtuve mi RAPIDAPI_KEY de RapidAPI
- [ ] ✅ Creé mi bot con @BotFather
- [ ] ✅ Obtuve mi TELEGRAM_BOT_TOKEN
- [ ] ✅ Envié un mensaje a mi bot
- [ ] ✅ Obtuve mi TELEGRAM_CHAT_ID
- [ ] ✅ Configuré los 3 secrets en GitHub
- [ ] ✅ Ejecuté el workflow manualmente
- [ ] ✅ Vi los logs sin errores
- [ ] ✅ Recibí ofertas en Telegram
- [ ] ✅ El bot funciona 🎉

---

## 🎉 ¡Listo!

Tu bot ahora:
- ✅ Se ejecuta automáticamente cada 6 horas
- ✅ Busca ofertas de empleo
- ✅ Analiza reputación de empresas
- ✅ Envía alertas a Telegram
- ✅ No envía duplicados
- ✅ Funciona 24/7 gratis

**¡Felicidades! Tu bot está completamente configurado y operativo.** 🚀

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los logs en GitHub Actions
2. Verifica que los 3 secrets estén configurados
3. Asegúrate de que los nombres sean exactos (MAYÚSCULAS)
4. Revisa la sección de "Solución de Problemas" arriba

---

**Última actualización:** Diciembre 20, 2025
