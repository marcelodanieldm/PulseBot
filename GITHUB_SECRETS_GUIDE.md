# 🔐 Guía de Configuración de GitHub Secrets

## 📋 Resumen

Para que PulseBot funcione automáticamente en GitHub Actions, necesitas configurar 3 **Secrets** (variables secretas) en tu repositorio de GitHub.

---

## 🛡️ ¿Qué son los GitHub Secrets?

Los Secrets son variables de entorno **encriptadas** que GitHub Actions puede usar durante la ejecución. **Nadie puede verlos**, ni siquiera tú después de guardarlos. Son la forma segura de guardar tokens y API keys.

---

## 📝 Paso a Paso: Configurar tus Secrets

### 1️⃣ Ir a la Configuración del Repositorio

1. Ve a tu repositorio: `https://github.com/marcelodanieldm/PulseBot`
2. Haz clic en **⚙️ Settings** (arriba a la derecha)
3. En el menú izquierdo, busca la sección **"Security"**
4. Haz clic en **"Secrets and variables"** → **"Actions"**

---

### 2️⃣ Crear los 3 Secrets Necesarios

Ahora vas a crear 3 secrets. Para cada uno:

#### 🔹 Secret 1: `RAPIDAPI_KEY`

1. Haz clic en **"New repository secret"** (botón verde)
2. En **Name**, escribe exactamente: `RAPIDAPI_KEY`
3. En **Secret**, pega tu API key de RapidAPI (JSearch)
   - **Dónde conseguirla:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
   - Ve a tu dashboard → Endpoints → Verás tu key: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
4. Haz clic en **"Add secret"**

---

#### 🔹 Secret 2: `TELEGRAM_BOT_TOKEN`

1. Haz clic en **"New repository secret"** nuevamente
2. En **Name**, escribe exactamente: `TELEGRAM_BOT_TOKEN`
3. En **Secret**, pega el token de tu bot de Telegram
   - **Dónde conseguirlo:** Habla con [@BotFather](https://t.me/BotFather) en Telegram
   - Formato: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
4. Haz clic en **"Add secret"**

---

#### 🔹 Secret 3: `TELEGRAM_CHAT_ID`

1. Haz clic en **"New repository secret"** por tercera vez
2. En **Name**, escribe exactamente: `TELEGRAM_CHAT_ID`
3. En **Secret**, pega el ID de tu canal/chat de Telegram
   - **Dónde conseguirlo:** 
     - Si es un canal: `-100xxxxxxxxxx` (formato con `-100` al inicio)
     - Si es un chat privado: Tu user ID numérico
   - **Truco para obtenerlo:** 
     1. Envía un mensaje a tu bot
     2. Visita: `https://api.telegram.org/bot<TU_BOT_TOKEN>/getUpdates`
     3. Busca el campo `"chat":{"id": -100xxxxxxxxx}`
4. Haz clic en **"Add secret"**

---

### 3️⃣ Verificar que los Secrets están Configurados

Después de agregar los 3 secrets, deberías ver en la página de Secrets:

```
✅ RAPIDAPI_KEY          Updated X minutes ago
✅ TELEGRAM_BOT_TOKEN    Updated X minutes ago
✅ TELEGRAM_CHAT_ID      Updated X minutes ago
```

> ⚠️ **Importante:** Los valores **no se pueden ver** después de crearlos. Solo puedes actualizarlos o eliminarlos.

---

## 🚀 Ejecutar el Workflow

### Ejecución Automática

El workflow se ejecutará automáticamente cada **4 horas** gracias al cron:
```yaml
schedule:
  - cron: '0 */4 * * *'
```

**Horarios (UTC):**
- 00:00 (12:00 AM)
- 04:00 (4:00 AM)
- 08:00 (8:00 AM)
- 12:00 (12:00 PM)
- 16:00 (4:00 PM)
- 20:00 (8:00 PM)

### Ejecución Manual

Para ejecutar el bot manualmente **ahora mismo**:

1. Ve a la pestaña **"Actions"** en tu repositorio
2. En el menú izquierdo, haz clic en **"PulseBot Automated Job Search"**
3. Haz clic en el botón **"Run workflow"** (arriba a la derecha)
4. Selecciona la rama `main`
5. Haz clic en **"Run workflow"** (botón verde)

---

## 📊 Monitorear la Ejecución

### Ver Logs en Tiempo Real

1. Ve a **Actions** en tu repo
2. Haz clic en la ejecución más reciente
3. Haz clic en el job **"run-pulsebot"**
4. Verás logs detallados de cada paso:
   - ✅ Instalación de dependencias
   - ✅ Ejecución de PulseBot
   - ✅ Commit y push de la base de datos

### Verificar que Funciona

Después de la primera ejecución exitosa:

1. **Telegram:** Deberías recibir ofertas de empleo en tu canal
2. **GitHub:** El archivo `processed_jobs.db` debería tener un nuevo commit automático:
   ```
   🤖 Update processed_jobs.db - 2024-12-20 08:00:00 UTC
   ```

---

## 🔧 Troubleshooting

### ❌ Error: "Resource not accessible by integration"

**Solución:** El workflow necesita permisos de escritura.

1. Ve a **Settings** → **Actions** → **General**
2. En **"Workflow permissions"**, selecciona:
   - ✅ **"Read and write permissions"**
3. Guarda los cambios

---

### ❌ Error: "Secrets not found"

**Solución:** Verifica que los nombres sean EXACTOS:
- ❌ `telegram_bot_token` (minúsculas)
- ❌ `TELEGRAM_TOKEN` (nombre diferente)
- ✅ `TELEGRAM_BOT_TOKEN` (correcto)

---

### ❌ Error: "Failed to push database"

**Solución:** Conflicto de git. El workflow tiene retry automático, pero si persiste:

1. Ve a tu repositorio local
2. Ejecuta:
   ```bash
   git pull origin main
   git push origin main
   ```
3. Vuelve a ejecutar el workflow manualmente

---

## 🎯 Checklist Final

Antes de ejecutar el workflow, verifica:

- [ ] Los 3 secrets están configurados en GitHub
- [ ] El archivo `.github/workflows/pulsebot_run.yml` existe
- [ ] El archivo `processed_jobs.db` existe en el repositorio
- [ ] Los permisos de GitHub Actions están en "Read and write"
- [ ] Has hecho `git push` de todos los archivos

---

## 📖 Archivos del Proyecto

```
PulseBot/
├── .github/
│   └── workflows/
│       └── pulsebot_run.yml      # ✅ Workflow de GitHub Actions
├── job_search.py                  # ✅ Script principal
├── processed_jobs.db              # ✅ Base de datos (se auto-actualiza)
├── requirements.txt               # ✅ Dependencias
├── .env                           # ⚠️ Solo para desarrollo local (ignorado en git)
├── .gitignore                     # ✅ Configuración de archivos ignorados
└── GITHUB_SECRETS_GUIDE.md        # 📖 Esta guía
```

---

## 🎉 ¡Listo!

Una vez configurados los Secrets, tu PulseBot:

- ✅ Se ejecutará automáticamente cada 4 horas
- ✅ Buscará ofertas de empleo con Business Intelligence
- ✅ Enviará notificaciones a Telegram
- ✅ Guardará la base de datos en GitHub (memoria persistente)
- ✅ Evitará enviar ofertas duplicadas

**¡Tu bot está 100% automatizado en la nube!** 🚀
