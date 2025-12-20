# 🤖 PulseBot - Job Search Automation v2.1.0

Bot inteligente que busca ofertas de empleo con **Business Intelligence Layer** y las envía a Telegram automáticamente.

## ✨ Características

### 🔍 Búsqueda Inteligente
- ✅ Búsqueda automatizada usando JSearch API (RapidAPI)
- ✅ Filtrado por criterios: Software Engineer, Remote, LatAm, Startups
- ✅ Filtrado por plataformas ATS: Greenhouse, Lever, BambooHR

### 🧠 Business Intelligence Layer (v2.1.0)
- ⭐ **Glassdoor Rating Extraction**: Rating automático de empresas (0.0-5.0)
- 🔥 **Growth Indicator**: Detecta empresas de alto crecimiento (>3 vacantes en 7 días)
- 💬 **Sentiment Analysis**: Análisis NLP de job descriptions (4 niveles)
- ⚡ **Pulse Score**: Métrica compuesta 1-10 para comparar ofertas
- 💡 **Tips Personalizados**: Recomendaciones inteligentes basadas en características

### 🏢 Clasificación Automática
- 🚀 **STARTUP**: Empresas en etapa de crecimiento
- 🏢 **FACTORY/STAFFING**: Consultoras y outsourcing
- 💳 **FINTECH/AI**: Fintech y tecnología de punta
- 📦 **GENERAL**: Resto de empresas

### 🎯 Detección de LatAm
- 🔥 Marca ofertas que buscan talento de LatAm explícitamente
- Palabras clave: "latin america", "latam", "argentina", "colombia", etc.

### 📊 Reputation Check
- 🔍 Búsqueda de employee reviews en DuckDuckGo
- 📈 Contador de vacantes activas por empresa
- 🤖 Indicador de probabilidad de contratación

### 🚀 Automatización Total
- ⏰ Ejecución automática cada 4 horas con GitHub Actions
- 💾 Persistencia de base de datos en Git (cero duplicados)
- 📱 Envío automático a Telegram
- ✅ 100% gratis con GitHub Actions (2000 min/mes)

## 🚀 Instalación y Deployment

### ⭐ Opción 1: Automatización con GitHub Actions (Recomendado)

**Tu bot se ejecutará automáticamente cada 4 horas en la nube - 100% GRATIS**

#### 📋 Requisitos Previos
- Cuenta de GitHub (gratuita)
- Bot de Telegram creado ([@BotFather](https://t.me/botfather))
- API Key de RapidAPI JSearch

#### 🎯 Guías de Deployment

1. **📖 [GITHUB_ACTIONS_DEPLOY.md](GITHUB_ACTIONS_DEPLOY.md)** - Guía rápida con checklist
2. **📖 [GITHUB_SECRETS_GUIDE.md](GITHUB_SECRETS_GUIDE.md)** - Guía detallada paso a paso

#### ⚡ Pasos Rápidos

1. **Configura 3 GitHub Secrets** (5 min)
   - Ve a: Settings → Secrets and variables → Actions
   - Agrega: `RAPIDAPI_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

2. **Habilita Permisos de Escritura** (1 min)
   - Settings → Actions → General
   - Workflow permissions → "Read and write permissions"

3. **Ejecuta el Workflow** (Primera vez)
   - Actions → "PulseBot Automated Job Search"
   - Run workflow → main

4. **¡Listo!** 🎉
   - El bot buscará ofertas cada 4 horas automáticamente
   - Recibirás notificaciones en Telegram con BI completo

---

### 💻 Opción 2: Ejecución Local

Para probar el bot localmente en tu computadora:

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd PulseBot
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Obtener API Key de JSearch (RapidAPI)

1. Ve a [RapidAPI - JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
2. Regístrate o inicia sesión
3. Suscríbete al plan gratuito (incluye 100 requests/mes)
4. Copia tu API Key (X-RapidAPI-Key)

### 2. Crear Bot de Telegram

1. Abre Telegram y busca [@BotFather](https://t.me/botfather)
2. Envía el comando `/newbot`
3. Sigue las instrucciones para crear tu bot
4. Guarda el **token** que te proporciona (ej: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Obtener Chat ID de Telegram

**Opción A: Chat personal**
1. Envía cualquier mensaje a tu bot
2. Visita en tu navegador: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Busca `"chat":{"id": XXXXXX}` y copia ese número

**Opción B: Canal o grupo**
1. Añade tu bot como administrador al canal/grupo
2. Envía un mensaje en el canal/grupo
3. Visita: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
4. Busca el `chat_id` (puede ser negativo, ej: `-1001234567890`)

### 4. Configurar variables de entorno

1. Copia el archivo de ejemplo:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Edita el archivo `.env` con tus credenciales:
```env
RAPIDAPI_KEY=tu_rapidapi_key_real
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=tu_chat_id_numerico
```

### Opción 2: Despliegue Automático en GitHub Actions (Recomendado) 🌟

**ACTUALIZADO A v2.1.0:** Ahora con automatización completa cada 4 horas

👉 **Deployment Rápido**: [GITHUB_ACTIONS_DEPLOY.md](GITHUB_ACTIONS_DEPLOY.md)  
👉 **Guía de Secrets**: [GITHUB_SECRETS_GUIDE.md](GITHUB_SECRETS_GUIDE.md)

#### ✨ Ventajas de GitHub Actions
- ⏰ Se ejecuta automáticamente cada 4 horas
- 💾 Base de datos persistente (cero duplicados)
- 🆓 100% gratis (2000 min/mes con GitHub)
- 🔒 Secrets seguros y encriptados
- 📊 Logs completos de cada ejecución
- 🚀 Sin servidor ni infraestructura que mantener

#### 🎯 Proceso de Setup (10 minutos)
1. Configura 3 GitHub Secrets (5 min)
2. Habilita permisos de escritura (1 min)
3. Ejecuta el workflow manualmente (primera vez)
4. ¡Listo! El bot trabajará solo 🎉

**Pasos rápidos:**
1. Sube el proyecto a GitHub
2. Configura 3 Secrets en GitHub: `RAPIDAPI_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
3. GitHub Actions se ejecutará automáticamente cada 6 horas
4. ¡Recibe ofertas sin hacer nada! 🎉

**Ventajas:**
- ✅ 100% gratuito (2000 minutos/mes en GitHub)
- ✅ Automático (sin intervención manual)
- ✅ No requiere servidor propio
- ✅ Sistema anti-duplicados integrado
- ✅ Logs y monitoreo incluidos
- ✅ Se ejecuta 24/7 en la nube

---

## 🎯 Uso

### Ver una demostración

Antes de configurar las APIs, puedes ver cómo funciona el sistema:

```bash
python demo.py
```

Esto te mostrará:
- Análisis de sentimiento en acción
- Contador de vacantes activas
- Cálculo de probabilidad de contratación
- Vista previa de mensajes de Telegram

### Ejecutar el script completo

```bash
python job_search.py
```

### Salida esperada

```
==================================================
🤖 PulseBot - Buscador de Empleos
==================================================

📋 Criterios de búsqueda:
  - Puesto: Software Engineer
  - Ubicación: Latin America
  - Tipo: Remote
  - Enfoque: Startups
  - Plataformas: Greenhouse, Lever, BambooHR

🔍 Buscando página 1...
✅ Encontrados 10 trabajos en página 1
🔍 Buscando página 2...
✅ Encontrados 10 trabajos en página 2
📊 Filtrados 8 de 20 trabajos por plataforma ATS
🚀 Filtrados 7 trabajos potenciales de startups

📤 Enviando 5 ofertas a Telegram...

[1/5] Enviando: Senior Software Engineer - Acme Corp
  ✅ Enviado correctamente
[2/5] Enviando: Backend Developer - TechStartup
  🔍 Analizando reputación de TechStartup...
  ✅ Enviado correctamente
...

==================================================
✨ Proceso completado: 5/5 ofertas enviadas
==================================================
```

### Formato de mensaje en Telegram

Cada oferta incluye **Business Intelligence completo**:

```
🔥 [🚀 STARTUP] Senior Full Stack Engineer

🏢 Empresa: Google
💰 Nicho: AI/ML
📍 Ubicación: Remote, Global
💰 $100,000 - $150,000 USD
🛠️ ATS: Lever

📊 Análisis de Empresa:
   • Vacantes activas: 5
   • Rating Glassdoor: 4.3/5 ⭐
   • 🔥 HIGH GROWTH: 5 vacantes en 7 días
   • Sentimiento: Positivo

🔥 Posibilidad de contratación: Alta

⚡ Pulse Score: [⭐⭐⭐⭐⭐⭐⭐⭐--] 8/10
💡 Tip: Esta empresa está escalando rápido, excelente rating
      - ¡Gran oportunidad! 🎯

🔗 Aplicar aquí: https://...
```

## ⚡ Pulse Score: Métrica Inteligente

El **Pulse Score** es una métrica compuesta (1-10) que evalúa cada oferta con 5 factores:

### 📊 Fórmula de Scoring

| Factor | Puntos | Condición |
|--------|--------|-----------|
| 🚀 Es STARTUP | +3 | Empresa en etapa de crecimiento |
| ⭐ Rating Alto | +2 | Glassdoor > 4.0/5.0 |
| 🔥 Alto Crecimiento | +3 | >2 vacantes activas |
| 🌎 LatAm Match | +2 | Busca talento LatAm explícitamente |
| 💬 Sentimiento Positivo | +1 | Job description muy positiva |
| ⚠️ Sentimiento Negativo | -1 | Job description negativa |

### 🎯 Interpretación del Score

- **8-10**: ¡Gran oportunidad! 🎯 - Aplica ya
- **6-7**: Vale la pena aplicar - Buena opción
- **4-5**: Investiga más antes de aplicar
- **1-3**: Procede con cautela

### 💡 Tips Personalizados

Cada score incluye un **tip personalizado** basado en las características detectadas:

```
Score 10/10:
"Esta empresa está escalando rápido, excelente rating (4.5/5),
 busca talento LatAm específicamente - ¡Gran oportunidad! 🎯"

Score 4/10:
"Revisa bien la descripción y cultura de la empresa
 - Investiga más antes de aplicar"
```

## 📝 Estructura del Proyecto

```
PulseBot/
├── .github/
│   └── workflows/
│       └── pulsebot_run.yml          # Workflow de GitHub Actions
├── job_search.py                      # Script principal con BI Layer
├── test_business_intelligence.py      # Tests de BI (6/6 passing)
├── test_clasificacion.py              # Tests de clasificación
├── test_github_actions.py             # Script de verificación
├── processed_jobs.db                  # Base de datos SQLite (auto-actualiza)
├── requirements.txt                   # Dependencias de Python
├── .env.example                       # Plantilla de configuración
├── .env                               # Tu configuración (NO subir a git)
├── .gitignore                         # Archivos ignorados por git
├── GITHUB_ACTIONS_DEPLOY.md           # Guía rápida de deployment
├── GITHUB_SECRETS_GUIDE.md            # Guía detallada de secrets
└── README.md                          # Este archivo
```

## 🔧 Personalización

### Cambiar criterios de búsqueda

Edita la función `main()` en [job_search.py](job_search.py):

```python
jobs = search_jobs(
    query="Python Developer startup",  # Cambia la búsqueda
    location="Argentina",               # Cambia la ubicación
    remote_jobs_only=True,             # True/False
    num_pages=3                        # Más páginas = más resultados
)
```

### Cambiar plataformas ATS

Edita la constante `ALLOWED_PLATFORMS` en [job_search.py](job_search.py):

```python
ALLOWED_PLATFORMS = ['greenhouse.io', 'lever.co', 'bamboohr.com', 'workable.com']
```

### Cambiar número de ofertas enviadas

Edita esta línea en `main()`:

```python
jobs_to_send = startup_jobs[:10]  # Cambia 5 por el número que quieras
```

## 📊 API Limits y Costos

### GitHub Actions (Cuenta Gratuita)
- ✅ 2000 minutos/mes GRATIS
- Cada ejecución: ~3 minutos
- 6 ejecuciones/día = 540 min/mes
- Sobran ~1460 min para otros workflows

### JSearch (Plan Gratuito)
- 100 requests/mes
- Cada búsqueda = 1 request
- ⚠️ 6 ejecuciones/día × 30 = 180 requests/mes (excede límite)
- 💡 **Solución**: Reduce a cada 6 horas (120 requests/mes)
  - O suscríbete al plan Basic (500 requests/mes)

### Telegram Bot API
- Sin límites para uso normal
- Rate limit: 30 mensajes/segundo

### DuckDuckGo Search
- Sin límites estrictos
- Incluye rate limiting automático
- No requiere API key
- **Nota**: Si aparece rate limit, el bot continúa sin reviews

## 📦 Dependencias

El proyecto usa las siguientes librerías:
- `requests`: Peticiones HTTP a APIs
- `python-dotenv`: Gestión de variables de entorno
- `duckduckgo-search`: Búsqueda web sin API key
- `textblob`: Análisis de sentimiento NLP
- `beautifulsoup4`: Parsing de HTML (utilidad)

## 🎯 Cómo funciona el Reputation Check

### 1. Búsqueda de Reviews
- Busca automáticamente "{Empresa} employee reviews glassdoor" en DuckDuckGo
- Prioriza resultados de Glassdoor, Indeed y Comparably
- Extrae snippets de hasta 200 caracteres

### 2. Análisis de Sentimiento
- Usa TextBlob para analizar la descripción del trabajo
- Clasifica el tono como: Positivo, Neutral o Negativo
- Ayuda a identificar empresas con cultura positiva

### 3. Contador de Vacantes Activas
- Cuenta cuántas posiciones tiene abiertas la empresa
- Más vacantes = mayor actividad de contratación
- Indicador de crecimiento y necesidad de talento

### 4. Probabilidad de Contratación
El algoritmo considera:
- **Vacantes activas** (peso mayor):
  - ≥5 vacantes: +3 puntos
  - ≥3 vacantes: +2 puntos
  - ≥2 vacantes: +1 punto
- **Reviews encontradas**: +1 punto
- **Sentimiento positivo**: +1 punto
- **Sentimiento negativo**: -1 punto

**Clasificación:**
- 🔥 **Alta** (≥4 puntos): Empresa activamente contratando
- ⚡ **Media** (2-3 puntos): Contratación moderada
- 💤 **Baja** (<2 puntos): Pocas vacantes o señales débiles

## 🐛 Solución de Problemas

### Error: "RAPIDAPI_KEY no configurada"
- Verifica que el archivo `.env` existe
- Asegúrate de que copiaste correctamente la API key (sin espacios)

### Error: "Credenciales de Telegram no configuradas"
- Verifica que `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` están en `.env`
- El chat ID debe ser numérico (puede ser negativo para grupos/canales)

### No se encuentran trabajos
- La API puede no tener resultados para esos criterios específicos
- Intenta ampliar la búsqueda (más páginas, criterios menos restrictivos)
- Verifica que tienes requests disponibles en tu plan de RapidAPI

### Los mensajes no llegan a Telegram
- Verifica que el bot no esté bloqueado
- Si es un canal, asegúrate de que el bot es administrador
- Verifica el chat ID (usa el método de `/getUpdates` nuevamente)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 📧 Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.

---

**¡Feliz búsqueda de empleo! 🎉**
