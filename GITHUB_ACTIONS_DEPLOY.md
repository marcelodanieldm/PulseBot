# 🚀 Guía Rápida: Deploy de PulseBot en GitHub Actions

## ✅ Estado Actual

Tu PulseBot está **100% listo** para automatizarse con GitHub Actions. Los archivos ya están creados:

- ✅ `.github/workflows/pulsebot_run.yml` - Workflow de GitHub Actions
- ✅ `GITHUB_SECRETS_GUIDE.md` - Guía detallada de configuración de secrets
- ✅ `test_github_actions.py` - Script de verificación local
- ✅ `.gitignore` - Configurado para permitir `processed_jobs.db`

---

## 📦 Paso 1: Subir Archivos a GitHub

Ejecuta estos comandos en tu terminal:

```bash
# Agregar los nuevos archivos
git add .github/workflows/pulsebot_run.yml
git add GITHUB_SECRETS_GUIDE.md
git add GITHUB_ACTIONS_DEPLOY.md
git add test_github_actions.py

# Verificar que processed_jobs.db está trackeado
git add processed_jobs.db

# Commitear
git commit -m "🤖 Add GitHub Actions automation - PulseBot v2.1.0"

# Pushear a GitHub
git push origin main
```

---

## 🔐 Paso 2: Configurar GitHub Secrets

### 📍 Ubicación en GitHub

1. Ve a tu repositorio: https://github.com/marcelodanieldm/PulseBot
2. Haz clic en **⚙️ Settings**
3. En el menú izquierdo: **Security** → **Secrets and variables** → **Actions**

### 🔑 Crear los 3 Secrets

Haz clic en **"New repository secret"** para cada uno:

#### Secret 1: `RAPIDAPI_KEY`
- **Name:** `RAPIDAPI_KEY` (exacto, mayúsculas)
- **Value:** Tu API key de RapidAPI (JSearch)
- 📖 Dónde conseguirla: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

#### Secret 2: `TELEGRAM_BOT_TOKEN`
- **Name:** `TELEGRAM_BOT_TOKEN` (exacto, mayúsculas)
- **Value:** Token de tu bot de Telegram
- 📖 Dónde conseguirlo: Habla con [@BotFather](https://t.me/BotFather)

#### Secret 3: `TELEGRAM_CHAT_ID`
- **Name:** `TELEGRAM_CHAT_ID` (exacto, mayúsculas)
- **Value:** ID de tu canal/chat de Telegram
- 📖 Truco: Envía un mensaje a tu bot y visita:
  ```
  https://api.telegram.org/bot<TU_BOT_TOKEN>/getUpdates
  ```
  Busca: `"chat":{"id": -100xxxxxxxxx}`

---

## ⚙️ Paso 3: Configurar Permisos de GitHub Actions

GitHub Actions necesita permisos para hacer commit de `processed_jobs.db`:

1. Ve a **Settings** → **Actions** → **General**
2. Baja hasta **"Workflow permissions"**
3. Selecciona: **✅ Read and write permissions**
4. Haz clic en **Save**

---

## 🧪 Paso 4: Probar el Workflow (Ejecución Manual)

### Primera Ejecución Manual

1. Ve a la pestaña **Actions** en tu repositorio
2. En el menú izquierdo, haz clic en **"PulseBot Automated Job Search"**
3. Haz clic en el botón **"Run workflow"** (arriba a la derecha)
4. Selecciona la rama **`main`**
5. Haz clic en **"Run workflow"** (botón verde)

### Monitorear la Ejecución

1. Haz clic en la ejecución que acaba de iniciar
2. Haz clic en el job **"run-pulsebot"**
3. Verás logs en tiempo real de cada paso:

```
📥 Checkout Repository         ✅
🐍 Setup Python 3.11            ✅
📦 Install Dependencies         ✅
🔍 Run PulseBot                 ✅
💾 Commit and Push Database     ✅
✅ Success Notification         ✅
```

---

## 📊 Paso 5: Verificar que Funciona

### ✅ Checklist de Verificación

- [ ] **Telegram:** Recibiste ofertas de empleo en tu canal
- [ ] **Business Intelligence:** Los mensajes incluyen:
  - Pulse Score con barra visual
  - Rating de Glassdoor (si disponible)
  - Indicador de HIGH GROWTH
  - Tip personalizado
- [ ] **GitHub:** El archivo `processed_jobs.db` tiene un nuevo commit:
  ```
  🤖 Update processed_jobs.db - 2024-12-20 08:00:00 UTC
  ```
- [ ] **Actions:** El workflow muestra estado verde ✅

---

## ⏰ Ejecución Automática

Una vez verificado, el bot se ejecutará automáticamente cada **4 horas**:

### Horarios (UTC)
```
00:00 AM  →  04:00 AM  →  08:00 AM
12:00 PM  →  04:00 PM  →  08:00 PM
```

### Convertir a tu Zona Horaria

Si estás en **América Latina** (UTC-3 a UTC-6), resta las horas:

**Ejemplo (UTC-5 Colombia/Perú):**
```
00:00 UTC = 7:00 PM del día anterior
04:00 UTC = 11:00 PM del día anterior
08:00 UTC = 3:00 AM
12:00 UTC = 7:00 AM
16:00 UTC = 11:00 AM
20:00 UTC = 3:00 PM
```

---

## 🔧 Troubleshooting

### ❌ Error: "Resource not accessible by integration"

**Causa:** Permisos de GitHub Actions no configurados

**Solución:**
1. Settings → Actions → General
2. Workflow permissions → **Read and write permissions**

---

### ❌ Error: "Secret RAPIDAPI_KEY not found"

**Causa:** Los secrets no están configurados o tienen nombre incorrecto

**Solución:**
- Verifica que los nombres son **EXACTOS** (mayúsculas)
- Los secrets deben ser:
  - `RAPIDAPI_KEY` (no `rapidapi_key`)
  - `TELEGRAM_BOT_TOKEN` (no `TELEGRAM_TOKEN`)
  - `TELEGRAM_CHAT_ID` (no `CHAT_ID`)

---

### ❌ Error: "Failed to push database"

**Causa:** Conflicto de Git

**Solución:**
```bash
# En tu repositorio local
git pull origin main --rebase
git push origin main

# Luego reintenta el workflow en GitHub
```

---

### ⚠️ Warning: Rate Limit en DuckDuckGo

**Causa:** DuckDuckGo limita búsquedas frecuentes (normal)

**Impacto:** Algunos ratings de Glassdoor pueden no extraerse

**Solución:** El sistema está diseñado para manejar esto. Los jobs se enviarán de todos modos, solo sin el rating de Glassdoor.

---

## 📁 Estructura Final del Proyecto

```
PulseBot/
├── .github/
│   └── workflows/
│       └── pulsebot_run.yml           # ✅ Workflow de GitHub Actions
├── job_search.py                       # ✅ Script principal con BI Layer
├── test_business_intelligence.py       # ✅ Tests de BI (6/6 passing)
├── test_clasificacion.py               # ✅ Tests de clasificación
├── test_github_actions.py              # ✅ Script de verificación
├── processed_jobs.db                   # ✅ Base de datos (se auto-actualiza)
├── requirements.txt                    # ✅ Dependencias Python
├── .env                                # ⚠️ Solo local (ignorado en git)
├── .gitignore                          # ✅ Configurado correctamente
├── GITHUB_SECRETS_GUIDE.md             # 📖 Guía detallada de secrets
├── GITHUB_ACTIONS_DEPLOY.md            # 📖 Esta guía
└── README.md                           # 📖 Documentación principal
```

---

## 🎯 Resumen: 3 Acciones Críticas

1. **Push a GitHub**
   ```bash
   git push origin main
   ```

2. **Configurar 3 Secrets en GitHub**
   - `RAPIDAPI_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

3. **Habilitar Permisos de Escritura**
   - Settings → Actions → Read and write permissions

---

## 🎉 ¡Felicidades!

Tu **PulseBot 2.1.0** con Business Intelligence Layer está completamente automatizado en GitHub Actions. 

### Lo que lograrás:

- ✅ **Automatización Total:** Ejecuciones cada 4 horas sin intervención
- ✅ **Inteligencia de Negocios:** Pulse Score, ratings, growth indicators
- ✅ **Persistencia en la Nube:** La base de datos se guarda automáticamente
- ✅ **Cero Duplicados:** SQLite trackea cada oferta enviada
- ✅ **Infraestructura Gratis:** GitHub Actions te da 2000 minutos/mes gratis

---

## 📚 Documentación Adicional

- 📖 [GITHUB_SECRETS_GUIDE.md](GITHUB_SECRETS_GUIDE.md) - Guía detallada paso a paso
- 🧠 [Business Intelligence Layer](job_search.py) - Funciones de BI
- 🧪 [Tests](test_business_intelligence.py) - Suite de pruebas (6/6 passing)

---

**¿Necesitas ayuda?** Revisa los logs en la pestaña **Actions** de GitHub. Cada paso muestra información detallada.

🚀 **¡Happy automating!**
