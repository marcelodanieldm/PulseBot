# 🤖 PulseBot - Job Search Automation

Bot automatizado que busca ofertas de empleo en JSearch API y las envía a Telegram.

## 📋 Características

- ✅ Búsqueda automatizada de empleos usando JSearch API (RapidAPI)
- ✅ Filtrado por criterios específicos: Software Engineer, Remote, LatAm, Startups
- ✅ Filtrado por plataformas ATS: Greenhouse, Lever, BambooHR
- ✅ **Reputation Check**: Análisis de salud de la empresa
  - 🔍 Búsqueda de employee reviews en DuckDuckGo
  - 📊 Análisis de sentimiento con TextBlob
  - 🔥 Indicador de probabilidad de contratación
  - 📈 Contador de vacantes activas por empresa
- ✅ Envío automático a canal/chat de Telegram
- ✅ Formateo atractivo de mensajes con toda la información relevante

## 🚀 Instalación

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

Cada oferta incluye:
- 🔵 Título del puesto
- 🏢 Empresa
- 📍 Ubicación
- 💰 Salario (si disponible)
- 🔗 Plataforma ATS
- 📊 **Análisis de Empresa**:
  - Número de vacantes activas
  - Sentimiento de la descripción
  - Review de empleados (si se encuentra)
- 🔥 **Posibilidad de contratación**: Alta/Media/Baja
- Link de aplicación

## 📝 Estructura del Proyecto

```
PulseBot/
├── job_search.py      # Script principal
├── requirements.txt   # Dependencias de Python
├── .env.example      # Plantilla de configuración
├── .env              # Tu configuración (NO subir a git)
├── .gitignore        # Archivos ignorados por git
└── README.md         # Este archivo
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

## 📊 API Limits

### JSearch (Plan Gratuito)
- 100 requests/mes
- Cada búsqueda = 1 request
- El script usa 2 requests por defecto (2 páginas)

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
