# ⚡ Guía de Inicio Rápido - PulseBot

## 🎬 Pasos para comenzar (5 minutos)

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 2. Ver la demo (opcional pero recomendado)
```bash
python demo.py
```
Esto te muestra cómo funciona el sistema sin necesitar APIs.

### 3. Obtener credenciales

#### 🔑 JSearch API (RapidAPI)
1. Ve a: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Regístrate (plan gratuito: 100 requests/mes)
3. Copia tu `X-RapidAPI-Key`

#### 🤖 Telegram Bot
1. Busca **@BotFather** en Telegram
2. Envía `/newbot` y sigue instrucciones
3. Guarda el **token** que recibes

#### 📱 Telegram Chat ID
1. Envía un mensaje a tu bot
2. Abre: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Copia el número en `"chat":{"id": XXXXXX}`

### 4. Configurar .env
```bash
copy .env.example .env
```

Edita `.env` con tus credenciales:
```env
RAPIDAPI_KEY=tu_clave_real_aqui
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...
TELEGRAM_CHAT_ID=123456789
```

### 5. ¡Ejecutar!
```bash
python job_search.py
```

## 📊 Qué esperar

El bot:
1. ✅ Buscará ofertas de Software Engineer en LatAm (Remote)
2. ✅ Filtrará por plataformas: Greenhouse, Lever, BambooHR
3. ✅ Priorizará startups
4. ✅ Analizará cada empresa:
   - Buscará reviews de empleados
   - Analizará sentimiento de la descripción
   - Contará vacantes activas
   - Calculará probabilidad de contratación
5. ✅ Enviará 5 ofertas a tu Telegram con análisis completo

## 🎯 Output esperado en Telegram

```
🔵 Senior Software Engineer

🏢 Empresa: TechStartup
📍 Ubicación: Remote, Buenos Aires
💰 $80,000 - $120,000 USD
🔗 Plataforma: Greenhouse

📊 Análisis de Empresa:
   • Vacantes activas: 6
   • Sentimiento: Positivo
   • Review: "Great culture, competitive salary..."

🔥 Posibilidad de contratación: Alta

Aplicar aquí: https://jobs.greenhouse.io/...
```

## 🔧 Personalización Rápida

### Cambiar criterios de búsqueda
Edita [job_search.py](job_search.py) línea ~260:
```python
jobs = search_jobs(
    query="Python Developer startup",  # Cambia el puesto
    location="Argentina",               # Cambia el país
    remote_jobs_only=True,             
    num_pages=3                        # Más páginas = más resultados
)
```

### Cambiar número de ofertas
Línea ~278:
```python
jobs_to_send = startup_jobs[:10]  # Cambia 5 por el número que quieras
```

### Añadir más plataformas ATS
Línea ~23:
```python
ALLOWED_PLATFORMS = ['greenhouse.io', 'lever.co', 'bamboohr.com', 'workable.com']
```

## 🆘 Problemas Comunes

### "RAPIDAPI_KEY no configurada"
→ Verifica que el archivo `.env` existe y tiene la clave correcta

### "No se encontraron trabajos"
→ La API puede no tener resultados. Intenta:
- Ampliar búsqueda (más páginas)
- Cambiar ubicación
- Quitar filtro de startups

### "Rate limit alcanzado" (DuckDuckGo)
→ Normal, el bot continúa sin reviews. Espera unos minutos y vuelve a intentar.

### Los mensajes no llegan a Telegram
→ Verifica:
- Token del bot correcto
- Chat ID correcto (puede ser negativo para grupos)
- El bot no esté bloqueado

## 📚 Recursos Adicionales

- [README.md](README.md) - Documentación completa
- [EJEMPLO_MENSAJE.md](EJEMPLO_MENSAJE.md) - Visuales del output
- [CHANGELOG.md](CHANGELOG.md) - Detalles técnicos de Reputation Check
- [demo.py](demo.py) - Demo sin necesidad de APIs
- [test_reputation.py](test_reputation.py) - Tests de funciones

## 💡 Tips Pro

1. **Ejecuta la demo primero** para entender el sistema
2. **Empieza con pocas ofertas** (2-3) para probar
3. **Monitorea los límites** de API (100 requests/mes en plan gratuito)
4. **Ajusta el delay** si ves muchos rate limits de DuckDuckGo
5. **Personaliza los criterios** para tu búsqueda específica

## 🎉 ¡Listo!

Ya tienes un bot inteligente que:
- 🔍 Busca ofertas automáticamente
- 📊 Analiza la salud de las empresas
- 🔥 Te dice qué tan probable es que te contraten
- 📱 Te envía todo directo a Telegram

**¡Buena suerte con tu búsqueda de empleo!** 🚀
