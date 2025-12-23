# 🧪 Guía de Pruebas - PulseBot Expandido

## 🎯 Objetivo
Esta guía te ayudará a probar el flujo completo del bot con las nuevas características expandidas.

## ✨ Nuevas Características

### 1. **Búsquedas Expandidas**
- **150+ queries** configuradas (antes: 68)
- **Búsquedas en español**: "Ingeniero de Software remoto", "Desarrollador Python remoto", etc.
- **Búsquedas en inglés**: Roles ampliados (Mobile, AI/ML, Data, etc.)
- **Más tecnologías**: Django, FastAPI, Spring Boot, Angular, Vue.js, GraphQL, etc.

### 2. **Integración Mejorada con RemoteOK**
- API gratuita sin límites
- Obtiene TODAS las ofertas disponibles (~200-500)
- Filtrado inteligente por keywords en español e inglés
- Manejo robusto de errores

### 3. **Manejo de Errores**
- Try-catch en todas las búsquedas de JSearch
- Continúa el flujo incluso si una fuente falla
- Mensajes informativos en cada paso

## 🚀 Pasos para Probar

### Paso 1: Verificar Configuración

Asegúrate de tener tus variables de entorno configuradas en `.env`:

```bash
RAPIDAPI_KEY=tu_key_aqui
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
```

### Paso 2: Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### Paso 3: Ejecutar Tests de Flujo

Ejecuta el script de pruebas para verificar que todo funciona:

```powershell
python test_busqueda_expandida.py
```

**Esto probará:**
- ✅ Búsquedas en JSearch (español e inglés)
- ✅ Integración con RemoteOK
- ✅ Operaciones de base de datos
- ✅ Filtrado por plataformas ATS

### Paso 4: Ejecutar Búsqueda Completa

Una vez que los tests pasen, ejecuta el flujo completo:

```powershell
python job_search.py
```

## 📊 Qué Esperar

### Salida Normal del Flujo:

```
🗄️ Inicializando base de datos...
✅ Base de datos inicializada
📊 Ofertas procesadas anteriormente: X

📋 Estrategia Multi-Source EXPANDIDA:
  📊 Total queries configuradas: 150
  
  🔥 FUENTE 1: JSearch API (15 búsquedas)
     - Prioridad: Worldwide + Latam + Español
     - Incluye: ES, EN, múltiples roles y tecnologías
  
  🌐 FUENTE 2: RemoteOK API (GRATIS, SIN LÍMITES)
     - API pública sin autenticación
     - Obtiene TODAS las ofertas remotas disponibles
     - Filtrado por keywords en español e inglés
  
  ✅ Total esperado: ~200-300 ofertas por ejecución
  🏢 Filtro ATS: 68 plataformas

🔍 [1/15] JSearch: 'Software Engineer remote worldwide'
  ✅ 10 resultados

🔍 [2/15] JSearch: 'Desarrollador Python remoto'
  ✅ 8 resultados

...

🌐 Complementando con RemoteOK (API gratuita, sin límites)...
  🔍 RemoteOK: Obteniendo todas las ofertas...
  ✅ 245 trabajos obtenidos de RemoteOK
  ✅ RemoteOK aportó 87 ofertas filtradas (de 245 totales)

📊 Total encontrado: 187 ofertas (165 únicas)
🏢 Filtradas por ATS: 89 ofertas
✨ Encontradas 45 ofertas nuevas para enviar
```

### Búsquedas que se Ejecutarán:

**Español (12 búsquedas):**
- "Ingeniero de Software remoto"
- "Desarrollador Full Stack remoto"
- "Desarrollador Backend remoto"
- "Desarrollador Frontend remoto"
- "Ingeniero QA remoto"
- "Desarrollador Python remoto"
- "Desarrollador React remoto"
- "Ingeniero DevOps remoto"
- "Desarrollador Node.js remoto"
- "Desarrollador Java remoto"
- "Ingeniero de Datos remoto"
- "Desarrollador Web3 remoto"

**Inglés (138 búsquedas):**
- Worldwide & Global searches
- Latin America specific
- Por país (Mexico, Chile, Colombia, Brasil, Argentina, etc.)
- Por tecnología (Django, FastAPI, Spring Boot, Angular, Vue.js, etc.)
- Por especialidad (Mobile, AI/ML, Data, Blockchain, QA, etc.)

## 🐛 Solución de Problemas

### Error: "No API key found"
**Solución:** Verifica que `.env` existe y tiene `RAPIDAPI_KEY=...`

### Error: "RemoteOK error"
**Solución:** Esto es normal si RemoteOK está temporalmente caído. El bot continuará con JSearch.

### Error: "No se encontraron trabajos"
**Solución:** 
1. Verifica tu cuota de API en RapidAPI
2. Prueba ejecutar `test_busqueda_expandida.py` para diagnóstico
3. Revisa si hay errores de red

### Advertencia: "Todas las ofertas ya fueron procesadas"
**Esto es normal:** Significa que el bot ya envió todas las ofertas disponibles. 
- Espera unas horas para que aparezcan nuevas ofertas
- O borra `processed_jobs.db` para reenviar todo (no recomendado en producción)

## 📈 Métricas de Rendimiento

### Antes de la Expansión:
- Queries: 68
- Fuentes: 2 (JSearch + RemoteOK limitado)
- Ofertas esperadas: ~100-150 por ejecución
- Idiomas: Solo inglés

### Después de la Expansión:
- Queries: 150 (**+120%**)
- Fuentes: 2 (JSearch + RemoteOK mejorado)
- Ofertas esperadas: ~200-300 por ejecución (**+100%**)
- Idiomas: Español + Inglés
- Manejo de errores: Robusto con try-catch

## 🎨 Ejemplos de Búsquedas Nuevas

### Tecnologías Modernas:
- "Django Developer remote"
- "FastAPI Developer remote"
- "GraphQL Developer remote"
- "Kubernetes Engineer remote"

### Mobile & Apps:
- "Mobile Developer remote"
- "React Native Developer remote"
- "Flutter Developer remote"

### Data & AI:
- "Data Scientist remote"
- "ML Engineer remote"
- "AI Engineer remote"

### Español:
- "Ingeniero de Software remoto"
- "Desarrollador Full Stack remoto"
- "Ingeniero DevOps remoto"

## ✅ Checklist de Pruebas

- [ ] Variables de entorno configuradas
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Tests ejecutados (`python test_busqueda_expandida.py`)
- [ ] Todos los tests pasaron
- [ ] Flujo completo ejecutado (`python job_search.py`)
- [ ] Ofertas recibidas en Telegram
- [ ] Base de datos actualizada

## 🚨 Notas Importantes

1. **Cuota de API**: JSearch tiene límites mensuales. El bot ahora usa solo 15 búsquedas para conservar cuota.

2. **RemoteOK**: Es gratuito y sin límites. Si falla, el bot continúa con JSearch.

3. **Rate Limiting**: Hay pausas de 2 segundos entre búsquedas de JSearch y 1 segundo para RemoteOK.

4. **Base de Datos**: No bores `processed_jobs.db` sin razón, contiene el historial de ofertas enviadas.

5. **Telegram**: Asegúrate de que tu bot puede enviar mensajes al chat especificado.

## 🎉 ¡Listo!

Si todos los tests pasan y ves ofertas en Telegram, ¡el bot está funcionando perfectamente!

Para ejecución automática, configura un cron job o GitHub Actions (ver `GITHUB_ACTIONS_DEPLOY.md`).
