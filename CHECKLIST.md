# ✅ Checklist de Configuración - PulseBot

## 📋 Antes de Comenzar

- [ ] Python 3.7+ instalado
- [ ] Conexión a internet activa
- [ ] Cuenta de Telegram

---

## 🔧 Paso 1: Instalación (2 minutos)

```bash
cd "c:\Users\danie\OneDrive\Escritorio\proyectos programacion\PulseBot"
pip install -r requirements.txt
python -m textblob.download_corpora
```

**Verificación:**
- [ ] Todas las dependencias instaladas sin errores
- [ ] TextBlob corpora descargados

---

## 🎬 Paso 2: Ver Demo (Opcional - 1 minuto)

```bash
python demo.py
```

**Verificación:**
- [ ] Demo ejecutada exitosamente
- [ ] Ves análisis de sentimiento funcionando
- [ ] Ves cálculo de probabilidad de contratación
- [ ] Entiendes el formato del mensaje

---

## 🔑 Paso 3: Obtener Credenciales (10-15 minutos)

### A. RapidAPI (JSearch)

1. Ve a: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Regístrate o inicia sesión
3. Haz clic en "Subscribe to Test"
4. Selecciona el plan "BASIC" (Gratis - 100 requests/mes)
5. Copia tu `X-RapidAPI-Key`

**Verificación:**
- [ ] Cuenta creada en RapidAPI
- [ ] Suscrito al plan gratuito de JSearch
- [ ] API Key copiada

**Tu API Key:** `_________________________________`

### B. Telegram Bot

1. Abre Telegram
2. Busca: **@BotFather**
3. Envía: `/newbot`
4. Nombre del bot: `PulseBot Job Search` (o el que prefieras)
5. Username: `tu_pulsebot_bot` (debe terminar en '_bot')
6. Copia el **token** que recibes

**Verificación:**
- [ ] Bot creado exitosamente
- [ ] Token recibido y copiado

**Tu Token:** `_________________________________`

### C. Telegram Chat ID

**Opción 1 - Chat Personal (Recomendado):**
1. Busca tu bot en Telegram (el que acabas de crear)
2. Envíale cualquier mensaje: "Hola"
3. Abre en navegador: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
   (Reemplaza `<TU_TOKEN>` con tu token real)
4. Busca: `"chat":{"id":XXXXXX`
5. Copia ese número

**Opción 2 - Canal o Grupo:**
1. Crea un canal/grupo en Telegram
2. Añade tu bot como administrador
3. Envía un mensaje en el canal/grupo
4. Abre: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
5. El chat_id será negativo (ej: -1001234567890)

**Verificación:**
- [ ] Mensaje enviado al bot
- [ ] Chat ID obtenido correctamente

**Tu Chat ID:** `_________________________________`

---

## ⚙️ Paso 4: Configurar Variables de Entorno (2 minutos)

```bash
# El archivo .env ya existe, solo necesitas editarlo
notepad .env
```

**Reemplaza los valores:**
```env
RAPIDAPI_KEY=tu_api_key_de_rapidapi_aqui
TELEGRAM_BOT_TOKEN=tu_token_del_bot_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
```

**Ejemplo real:**
```env
RAPIDAPI_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

**Verificación:**
- [ ] Archivo `.env` editado
- [ ] RAPIDAPI_KEY configurada (sin comillas)
- [ ] TELEGRAM_BOT_TOKEN configurado (sin comillas)
- [ ] TELEGRAM_CHAT_ID configurado (sin comillas)
- [ ] No hay espacios extra ni caracteres raros

---

## 🧪 Paso 5: Prueba Básica (1 minuto)

```bash
python test_reputation.py
```

**Verificación:**
- [ ] Script ejecutado sin errores críticos
- [ ] Análisis de sentimiento funciona
- [ ] Cálculo de probabilidad funciona
- [ ] Si hay "Rate limit" en reviews, es normal

---

## 🚀 Paso 6: Ejecutar el Bot (¡Momento de la verdad!)

```bash
python job_search.py
```

**Qué deberías ver:**
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
✅ Encontrados X trabajos en página 1
...
```

**Verificación:**
- [ ] Script inició correctamente
- [ ] No hay errores de credenciales
- [ ] Búsqueda en JSearch API funciona
- [ ] Filtrado de trabajos ejecutado
- [ ] Mensajes enviándose a Telegram
- [ ] Recibes mensajes en Telegram

---

## 📱 Paso 7: Verificar Mensajes en Telegram

Abre Telegram y verifica que recibes mensajes como:

```
🔵 [Título del Puesto]

🏢 Empresa: [Nombre]
📍 Ubicación: [Ciudad, País]
💰 [Salario]
🔗 Plataforma: [ATS]

📊 Análisis de Empresa:
   • Vacantes activas: [Número]
   • Sentimiento: [Positivo/Neutral/Negativo]
   • Review: "[Texto]..."

🔥 Posibilidad de contratación: [Alta/Media/Baja]

Aplicar aquí: [Link]
```

**Verificación:**
- [ ] Recibo al menos 1 mensaje
- [ ] Formato correcto con emojis
- [ ] Toda la información visible
- [ ] Links funcionan
- [ ] Análisis de empresa incluido

---

## 🎉 ¡Felicidades! El Bot Está Funcionando

### ✅ Si todo funcionó:
1. **Guarda** tus credenciales en un lugar seguro
2. **Personaliza** los criterios de búsqueda si quieres
3. **Ejecuta** regularmente para nuevas ofertas
4. **Comparte** el proyecto si te fue útil

### ❌ Si algo falló:

#### Error: "RAPIDAPI_KEY no configurada"
- [ ] Verifica que `.env` existe
- [ ] Verifica que la key está sin comillas
- [ ] Verifica que no hay espacios extra

#### Error: "Credenciales de Telegram no configuradas"
- [ ] Verifica el token del bot
- [ ] Verifica el chat ID (puede ser negativo)
- [ ] Intenta obtener el chat ID nuevamente

#### Error: "No se encontraron trabajos"
- [ ] Normal si la API no tiene resultados para esos criterios
- [ ] Intenta ampliar la búsqueda
- [ ] Verifica que tienes requests disponibles en RapidAPI

#### Los mensajes no llegan a Telegram
- [ ] Verifica que el bot no esté bloqueado
- [ ] Verifica el chat ID nuevamente con /getUpdates
- [ ] Si es un canal, verifica que el bot es administrador

#### "Rate limit" en DuckDuckGo
- [ ] Normal, el bot continúa sin reviews
- [ ] Espera unos minutos entre ejecuciones

---

## 📊 Métricas de Éxito

Al final de una ejecución exitosa deberías ver:

```
==================================================
✨ Proceso completado: 5/5 ofertas enviadas
==================================================
```

- [ ] 5 ofertas enviadas correctamente
- [ ] Todas con análisis de empresa
- [ ] Sin errores críticos

---

## 🔄 Uso Regular

Para ejecutar el bot regularmente:

```bash
# Windows - Una vez
python job_search.py

# Windows - Cada día a las 9 AM (Task Scheduler)
# Crea una tarea programada que ejecute:
# C:\Python\python.exe "ruta\al\job_search.py"
```

---

## 📚 Recursos de Ayuda

- [ ] [README.md](README.md) - Documentación completa
- [ ] [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- [ ] [EJEMPLO_MENSAJE.md](EJEMPLO_MENSAJE.md) - Ejemplos visuales
- [ ] [CHANGELOG.md](CHANGELOG.md) - Detalles técnicos

---

## 💡 Tips Adicionales

1. **Primeras ejecuciones:** Empieza con pocas ofertas para probar
2. **Límites de API:** Monitorea tu uso en RapidAPI dashboard
3. **Personalización:** Ajusta criterios en `job_search.py`
4. **Rate Limiting:** Si ves muchos rate limits, aumenta los delays
5. **Feedback:** Las reviews de DuckDuckGo son un bonus, no críticas

---

```
╔════════════════════════════════════════════════╗
║                                                ║
║      ✅ Checklist Completado                  ║
║      🚀 PulseBot Operativo                    ║
║      🎯 Listo para Buscar Ofertas             ║
║                                                ║
╚════════════════════════════════════════════════╝
```

**¡Buena suerte con tu búsqueda de empleo!** 🎉
