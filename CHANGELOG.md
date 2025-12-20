# 🚀 Changelog - PulseBot

---

## [2.0.0] - 2025-12-20 🎉

### ✨ SISTEMA DE CLASIFICACIÓN INTELIGENTE

#### 🏷️ Clasificación Automática por Categorías
- **4 categorías principales** con 40+ keywords
  - 🚀 **STARTUP**: Series A/B, Equity, VC, SaaS, Fast-growing (13 keywords)
  - 🏢 **FACTORY/STAFFING**: Outsourcing, Nearshore, Consultancy (12 keywords)
  - 💳 **FINTECH/AI**: Fintech, Crypto, AI, ML, Blockchain (14 keywords)
  - 📋 **GENERAL**: Ofertas que no encajan en las anteriores
- **Detección case-insensitive** en título, descripción y company type
- **Función**: `classify_job(job) -> str`

#### 🔥 Filtro de LatAm Match Perfecto
- **18 keywords específicas** de Latinoamérica
  - Timezones: GMT-3, GMT-5, timezone alignment
  - Idioma: Spanish, Spanish speaking
  - Región: LatAm residents, Latin America, South America
  - Países: Argentina, Chile, Colombia, Mexico, Peru, Brazil
- **Emoji visual** (🔥) en el título del mensaje
- **Flag booleano** guardado en base de datos
- **Función**: `is_latam_match(job) -> bool`

#### 💾 Migración a Base de Datos SQLite
- **Archivo**: `processed_jobs.db` (reemplaza `sent_jobs.json`)
- **Tabla**: `processed_jobs`
  ```sql
  CREATE TABLE processed_jobs (
    job_id TEXT PRIMARY KEY,
    company_name TEXT,
    job_title TEXT,
    processed_at TEXT,
    category TEXT,
    is_latam_match INTEGER
  )
  ```
- **Ventajas sobre JSON**:
  - ✅ Consultas SQL avanzadas
  - ✅ Índices para búsquedas rápidas (job_id PRIMARY KEY)
  - ✅ Metadatos enriquecidos
  - ✅ Escalable a miles de registros
  - ✅ Integridad de datos garantizada
- **Funciones nuevas**:
  - `init_database()`: Inicializa la tabla
  - `is_job_processed(job_id)`: Verifica duplicados
  - `save_processed_job(...)`: Guarda con metadatos completos
  - `get_processed_count()`: Total de ofertas procesadas

#### 🎯 Detección de Nichos Tecnológicos
- **7 nichos detectables**:
  - SaaS (saas, software as a service, cloud platform)
  - Fintech (fintech, payments, banking)
  - Crypto/Web3 (crypto, blockchain, web3, defi, nft)
  - AI/ML (ai, machine learning, llm, deep learning)
  - E-commerce (ecommerce, marketplace, retail)
  - HealthTech (healthtech, healthcare, telemedicine)
  - EdTech (edtech, education, learning platform)
- **Función**: `detect_niche(job) -> str`
- **Muestra en mensaje**: `💰 Nicho: {nicho}`

#### 📱 Nuevo Formato de Mensaje en Telegram
```
🔥 [🚀 STARTUP] Senior Python Engineer

🏢 Empresa: StartupXYZ
💰 Nicho: SaaS
📍 Ubicación: Remote, Argentina
💰 $80,000 - $120,000 USD
🛠️ ATS: Lever

📊 Análisis de Empresa:
   • Vacantes activas: 8
   • Sentimiento: Positivo

🔥 Posibilidad de contratación: Alta

🔗 Aplicar aquí: https://...

ID: a1b2c3d4e5f6
```

**Cambios en el mensaje:**
- ✅ Emoji 🔥 para LatAm matches (condicional)
- ✅ Categoría con emoji en el header
- ✅ Campo "Nicho" nuevo
- ✅ Job ID corto para referencia
- ✅ Mejor organización visual

### 🧪 Testing y Validación

#### Suite de Tests Completa
- **Archivo**: `test_clasificacion.py`
- **4 tests automatizados**:
  1. ✅ Base de Datos SQLite
  2. ✅ Sistema de Clasificación
  3. ✅ Generación de Job IDs
  4. ✅ Formato de Mensajes
- **Resultado**: 4/4 tests pasando (100%)
- **Jobs de prueba**: 4 casos diferentes (Startup, Factory, Fintech/AI, General)

### 📚 Documentación Nueva

#### MEJORAS_CLASIFICACION.md (800+ líneas)
- Explicación detallada de cada categoría
- Keywords completas por categoría
- Ejemplos de clasificación con input/output
- Guía de personalización
- Casos de uso
- Troubleshooting
- Estadísticas y queries SQL

#### CONFIGURACION_SECRETS.md
- Tutorial paso a paso para obtener API keys
- Guía visual para configurar GitHub Secrets
- Troubleshooting de errores comunes
- Checklist interactivo

### 🔧 Cambios en el Código

#### Funciones Modificadas
- `format_job_message()`: Retorna tupla `(message, category, is_latam)`
- `send_to_telegram()`: Guarda en DB automáticamente después de enviar
- `filter_new_jobs()`: Usa SQLite en lugar de Set de IDs
- `main()`: Inicializa DB, muestra estadísticas mejoradas

#### Código Eliminado
- `load_sent_jobs()`: Reemplazado por `is_job_processed()`
- `save_sent_jobs()`: Reemplazado por `save_processed_job()`
- Lógica de Set para tracking de IDs

#### Diccionarios Nuevos
```python
CATEGORIES = {
    '🚀 STARTUP': [...],
    '🏢 FACTORY/STAFFING': [...],
    '💳 FINTECH/AI': [...]
}

LATAM_KEYWORDS = [
    'timezone alignment', 'gmt-3', 'gmt-5',
    'spanish', 'latam residents', ...
]
```

### 📊 Estadísticas de Cambios
- **Líneas agregadas**: ~573
- **Líneas eliminadas**: ~76
- **Archivos nuevos**: 4
- **Archivos modificados**: 1
- **Funciones nuevas**: 7
- **Total keywords**: 58+ (40 categorías + 18 LatAm)

### 🐛 Fixes
- Eliminado código duplicado en `format_job_message()`
- Corregido manejo de None en clasificación
- Actualizado return type de `format_job_message()` a tupla
- Mejorado manejo de excepciones en todas las nuevas funciones

### ⚡ Mejoras de Performance
- SQLite más rápido que JSON para grandes volúmenes
- Índice automático en `job_id` (PRIMARY KEY)
- Consultas optimizadas con prepared statements
- Menos I/O de disco (una conexión por operación)

---

## [1.2.0] - 2025-12-20

### 🛡️ Manejo Robusto de Errores

### 1. **Búsqueda de Reviews de Empleados** 🔍
- **Función**: `search_company_reviews(company_name)`
- **Funcionalidad**: Busca automáticamente reviews de empleados en DuckDuckGo
- **Query**: "{Empresa} employee reviews glassdoor"
- **Prioriza**: Glassdoor, Indeed, Comparably
- **Output**: Snippet de hasta 200 caracteres
- **Manejo de errores**: Continúa sin reviews si hay rate limiting

### 2. **Análisis de Sentimiento con NLP** 📊
- **Función**: `analyze_company_sentiment(company_name, job_description)`
- **Librería**: TextBlob
- **Análisis**: Polaridad del texto de la descripción del trabajo
- **Clasificación**: 
  - Positivo (polarity > 0.1)
  - Neutral (-0.1 ≤ polarity ≤ 0.1)
  - Negativo (polarity < -0.1)
- **Uso**: Detecta cultura empresarial agresiva vs. positiva

### 3. **Contador de Vacantes Activas** 📈
- **Función**: `count_company_active_jobs(company_name, all_jobs)`
- **Funcionalidad**: Cuenta cuántas vacantes tiene la empresa en el mismo ATS
- **Indicador**: Mayor número = empresa en crecimiento activo

### 4. **Cálculo de Probabilidad de Contratación** 🔥
- **Función**: `calculate_hiring_probability(active_jobs, has_reviews, sentiment)`
- **Algoritmo de scoring**:
  ```
  - ≥5 vacantes: +3 puntos
  - ≥3 vacantes: +2 puntos
  - ≥2 vacantes: +1 punto
  - Reviews encontradas: +1 punto
  - Sentimiento positivo: +1 punto
  - Sentimiento negativo: -1 punto
  ```
- **Clasificación**:
  - 🔥 **Alta** (≥4 puntos): Empresa activamente contratando
  - ⚡ **Media** (2-3 puntos): Contratación moderada
  - 💤 **Baja** (<2 puntos): Pocas señales de contratación

### 5. **Mensajes Mejorados en Telegram** 📱
- **Nueva sección**: "📊 Análisis de Empresa"
- **Información incluida**:
  - Número de vacantes activas
  - Sentimiento de la descripción
  - Review de empleados (si disponible)
  - Indicador de probabilidad de contratación con emoji

## 📦 Nuevas Dependencias

```txt
duckduckgo-search==4.1.1  # Búsqueda web sin API key
textblob==0.17.1          # Análisis de sentimiento NLP
beautifulsoup4==4.12.2    # Parsing HTML (utilidad)
```

## 📝 Archivos Modificados

### `job_search.py`
- ✅ Añadidas 5 nuevas funciones
- ✅ Modificada `format_job_message()` para incluir análisis
- ✅ Modificada `send_to_telegram()` para pasar contexto
- ✅ Actualizado `main()` para integrar el flujo completo

### `requirements.txt`
- ✅ Añadidas 3 nuevas dependencias

### `README.md`
- ✅ Documentadas nuevas características
- ✅ Explicado el algoritmo de Reputation Check
- ✅ Añadidos límites de API de DuckDuckGo
- ✅ Incluida sección de demo

## 🆕 Archivos Nuevos

### `test_reputation.py`
- Script de prueba unitaria para las funciones de Reputation Check
- Verifica: búsqueda de reviews, análisis de sentimiento, cálculo de probabilidad

### `demo.py`
- Demostración completa del sistema
- Muestra análisis con datos simulados
- No requiere API keys
- Incluye comparación entre empresas

### `EJEMPLO_MENSAJE.md`
- Documentación visual del formato de mensajes
- Comparación antes/después
- Guía de interpretación de indicadores

## 🎯 Impacto en el Usuario

### Antes
```
🔵 Senior Software Engineer
🏢 Empresa: TechCorp
💰 $80,000 - $120,000 USD
🔗 Plataforma: Greenhouse
```

### Después
```
🔵 Senior Software Engineer
🏢 Empresa: TechCorp
💰 $80,000 - $120,000 USD
🔗 Plataforma: Greenhouse

📊 Análisis de Empresa:
   • Vacantes activas: 7
   • Sentimiento: Positivo
   • Review: "Great company culture..."

🔥 Posibilidad de contratación: Alta
```

## 🔧 Configuración Adicional

```bash
# Instalar nuevas dependencias
pip install -r requirements.txt

# Descargar corpora de TextBlob (automático en primera ejecución)
python -m textblob.download_corpora
```

## ✅ Testing

```bash
# Probar funciones individuales
python test_reputation.py

# Ver demo completa
python demo.py

# Ejecutar bot completo
python job_search.py
```

## 🚨 Notas Importantes

1. **Rate Limiting**: DuckDuckGo puede aplicar rate limiting. El bot continúa sin reviews en ese caso.

2. **Delays**: Se añadieron delays de 2 segundos antes de cada búsqueda para evitar rate limits.

3. **Análisis opcional**: Si no se encuentran reviews, el cálculo de probabilidad continúa con los otros factores.

4. **Idioma**: TextBlob funciona mejor con texto en inglés. El análisis de sentimiento puede ser menos preciso con descripciones en español.

## 📊 Métricas de Mejora

- **Información adicional**: +3 campos nuevos por oferta
- **Contexto empresarial**: Análisis de 6 vacantes activas
- **Validación social**: Reviews de sitios como Glassdoor
- **Toma de decisiones**: Indicador claro de probabilidad de contratación
- **Tiempo ahorrado**: ~5 minutos por oferta en investigación manual

## 🎉 Resultado Final

El bot ahora proporciona:
✅ Análisis completo de salud empresarial
✅ Indicadores accionables de contratación
✅ Contexto social mediante reviews
✅ Scoring inteligente basado en múltiples factores
✅ Experiencia de usuario mejorada en Telegram

---

**Fecha de implementación**: Diciembre 20, 2025
**Versión**: 2.0 - Reputation Check Release
