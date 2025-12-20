# 🚀 Mejoras de Clasificación Inteligente - PulseBot

## 📋 Resumen de Mejoras

PulseBot ahora cuenta con un **sistema de clasificación inteligente** que detecta automáticamente el tipo de empresa, nicho tecnológico y ofertas perfectas para LatAm.

---

## ✨ Nuevas Características

### 1. 🏷️ **Sistema de Clasificación por Categorías**

El bot ahora clasifica automáticamente cada oferta en 4 categorías:

#### 🚀 **STARTUP**
Empresas en etapas tempranas con alto potencial de crecimiento.

**Keywords detectadas:**
- Series A, Series B, Seed
- Equity, Stock Options
- Unicorn, Venture Capital, VC
- Early Stage, Fast-growing, Scaling
- SaaS, Product-led
- Growth stage, Startup

**Ejemplo de detección:**
```
"We're a Series B SaaS startup offering equity compensation..."
→ Clasificado como: 🚀 STARTUP
```

---

#### 🏢 **FACTORY/STAFFING**
Empresas de outsourcing y staff augmentation.

**Keywords detectadas:**
- Outsourcing, Staff Augmentation
- Client project, Consultancy
- Digital Agency
- Nearshore, Offshore
- Managed services, B2B Services
- Staffing, Consulting

**Ejemplo de detección:**
```
"Join our nearshore consulting team working on client projects..."
→ Clasificado como: 🏢 FACTORY/STAFFING
```

---

#### 💳 **FINTECH/AI**
Empresas de tecnología financiera e inteligencia artificial (nichos de alto interés).

**Keywords detectadas:**
- Fintech, Payments, Banking
- Crypto, Web3, Blockchain, DeFi, NFT
- LLM, Machine Learning, AI
- Artificial Intelligence, Deep Learning
- Neural Network, Cryptocurrency

**Ejemplo de detección:**
```
"We're building the next generation of AI-powered fintech solutions..."
→ Clasificado como: 💳 FINTECH/AI
```

---

#### 📋 **GENERAL**
Ofertas que no coinciden con categorías específicas.

**Cuándo se asigna:**
- No se detectan keywords de las categorías anteriores
- Empresas tradicionales
- Roles corporativos estándar

---

### 2. 🔥 **Filtro de LatAm Match Perfecto**

El bot detecta ofertas **específicamente diseñadas para talento de Latinoamérica** y las marca con un emoji de fuego (🔥).

**Keywords de LatAm Match:**
- `Timezone alignment`
- `GMT-3`, `GMT-5`
- `Spanish`, `Spanish speaking`
- `LatAm residents`, `LatAm only`, `LatAm preferred`
- `Latin America`, `South America`
- `Timezone friendly`
- Países: `Argentina`, `Chile`, `Colombia`, `Mexico`, `Peru`, `Brazil`

**Ejemplo en Telegram:**
```
🔥 [🚀 STARTUP] Senior Python Engineer

🏢 Empresa: TechStartup Inc.
💰 Nicho: SaaS
📍 Ubicación: Remote, Latin America
💰 $80,000 - $120,000 USD
🛠️ ATS: Greenhouse
...
```

> **Nota:** El emoji 🔥 solo aparece si la oferta menciona específicamente keywords de LatAm.

---

### 3. 💾 **Base de Datos SQLite (processed_jobs.db)**

**Migración de JSON a SQLite:**

#### ❌ Antes (sent_jobs.json):
```json
{
  "sent_job_ids": ["abc123", "def456"],
  "last_updated": "2025-12-20 10:30:00 UTC",
  "total_sent": 2
}
```

**Limitaciones:**
- Archivo de texto plano
- Sin consultas avanzadas
- Difícil de analizar
- No tiene metadatos enriquecidos

#### ✅ Ahora (processed_jobs.db):

**Tabla:** `processed_jobs`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `job_id` | TEXT PRIMARY KEY | Hash MD5 único del trabajo |
| `company_name` | TEXT | Nombre de la empresa |
| `job_title` | TEXT | Título del puesto |
| `processed_at` | TEXT | Timestamp UTC del procesamiento |
| `category` | TEXT | Categoría detectada (🚀 STARTUP, etc.) |
| `is_latam_match` | INTEGER | 1 si es LatAm match, 0 si no |

**Ventajas:**
- ✅ Consultas SQL avanzadas
- ✅ Índices para búsquedas rápidas
- ✅ Metadatos enriquecidos (categoría, LatAm match)
- ✅ Análisis histórico detallado
- ✅ Escalable (miles de registros sin problemas)
- ✅ Integridad de datos garantizada

**Funciones implementadas:**
```python
init_database()                    # Crea la tabla si no existe
is_job_processed(job_id)          # Verifica si ya fue procesado
save_processed_job(...)           # Guarda con metadatos
get_processed_count()             # Total de ofertas en DB
```

---

### 4. 🎯 **Detección de Nicho Tecnológico**

El bot detecta automáticamente el nicho específico de cada oferta:

#### Nichos Detectables:

| Nicho | Keywords |
|-------|----------|
| **SaaS** | saas, software as a service, cloud platform, b2b software |
| **Fintech** | fintech, payments, banking, financial technology |
| **Crypto/Web3** | crypto, blockchain, web3, defi, nft |
| **AI/ML** | ai, machine learning, artificial intelligence, llm, deep learning |
| **E-commerce** | e-commerce, ecommerce, marketplace, retail |
| **HealthTech** | healthtech, healthcare, medical, telemedicine |
| **EdTech** | edtech, education, learning platform, online courses |
| **General** | (default si no se detecta nicho específico) |

**Ejemplo en mensaje:**
```
💰 Nicho: AI/ML
```

---

### 5. 📱 **Nuevo Formato de Mensaje en Telegram**

#### ✨ Formato Mejorado:

```
🔥 [💳 FINTECH/AI] Senior Backend Engineer

🏢 Empresa: FinTechCorp
💰 Nicho: Fintech
📍 Ubicación: Remote, Argentina
💰 $90,000 - $130,000 USD
🛠️ ATS: Lever

📊 Análisis de Empresa:
   • Vacantes activas: 8
   • Sentimiento: Positivo
   • Review: "Great company culture and benefits..."

🔥 Posibilidad de contratación: Alta

🔗 Aplicar aquí: https://jobs.lever.co/fintechcorp/abc123

ID: a1b2c3d4e5f6
────────────────────────────────────────
```

#### Elementos del mensaje:

1. **🔥 Emoji de LatAm Match** (condicional)
   - Solo aparece si la oferta menciona keywords de LatAm

2. **[Categoría] Título**
   - 🚀 STARTUP
   - 🏢 FACTORY/STAFFING
   - 💳 FINTECH/AI
   - 📋 GENERAL

3. **Información de la empresa:**
   - 🏢 Empresa
   - 💰 Nicho (nuevo!)
   - 📍 Ubicación
   - 💰 Salario
   - 🛠️ ATS Platform

4. **Análisis de reputación:**
   - Vacantes activas
   - Sentimiento
   - Reviews
   - Probabilidad de contratación

5. **ID único** (nuevo!)
   - Hash corto para referencia
   - Útil para reportar duplicados

---

## 🔍 Ejemplos de Clasificación

### Ejemplo 1: Startup con LatAm Match

**Input (JSearch API):**
```json
{
  "job_title": "Senior Full Stack Engineer",
  "employer_name": "StartupXYZ",
  "job_description": "We're a Series A startup building a SaaS platform. 
                      Looking for engineers in GMT-3 timezone. Spanish fluency required.",
  "job_country": "Remote"
}
```

**Output (Telegram):**
```
🔥 [🚀 STARTUP] Senior Full Stack Engineer

🏢 Empresa: StartupXYZ
💰 Nicho: SaaS
📍 Ubicación: Remote
...
```

**Análisis:**
- ✅ Detectó "Series A" → STARTUP
- ✅ Detectó "SaaS" → Nicho SaaS
- ✅ Detectó "GMT-3" + "Spanish" → LatAm Match (🔥)

---

### Ejemplo 2: Outsourcing (Factory)

**Input:**
```json
{
  "job_title": "Java Developer",
  "employer_name": "TechConsulting Inc",
  "job_description": "Join our nearshore team working on client projects. 
                      Staff augmentation model.",
  "job_country": "Multiple"
}
```

**Output:**
```
[🏢 FACTORY/STAFFING] Java Developer

🏢 Empresa: TechConsulting Inc
💰 Nicho: General
📍 Ubicación: Multiple
...
```

**Análisis:**
- ✅ Detectó "nearshore" + "client projects" + "staff augmentation" → FACTORY/STAFFING
- ⚠️ No hay keywords de LatAm específicas → Sin 🔥

---

### Ejemplo 3: Fintech/AI

**Input:**
```json
{
  "job_title": "Machine Learning Engineer",
  "employer_name": "CryptoBank",
  "job_description": "Build AI-powered fintech solutions using LLMs. 
                      Experience with blockchain and crypto payments required.",
  "job_country": "Remote"
}
```

**Output:**
```
[💳 FINTECH/AI] Machine Learning Engineer

🏢 Empresa: CryptoBank
💰 Nicho: Crypto/Web3
📍 Ubicación: Remote
...
```

**Análisis:**
- ✅ Detectó múltiples keywords: "fintech", "AI", "LLMs", "blockchain", "crypto" → FINTECH/AI
- ✅ Nicho detectado: Crypto/Web3 (más específico que Fintech)

---

## 📊 Estadísticas de Clasificación

El bot mantiene estadísticas en la base de datos:

```python
# Obtener total de ofertas procesadas
total = get_processed_count()
print(f"Total: {total} ofertas")

# Query SQL para ver distribución por categoría (ejemplo)
SELECT category, COUNT(*) as count 
FROM processed_jobs 
GROUP BY category;
```

**Ejemplo de output:**
```
🚀 STARTUP:          45 ofertas (38%)
🏢 FACTORY/STAFFING: 30 ofertas (25%)
💳 FINTECH/AI:       28 ofertas (23%)
📋 GENERAL:          17 ofertas (14%)
```

**LatAm Matches:**
```
SELECT COUNT(*) FROM processed_jobs WHERE is_latam_match = 1;
→ 22 ofertas (18% del total)
```

---

## 🛠️ Configuración y Uso

### 1. Instalación

No se requieren paquetes adicionales. SQLite viene incluido con Python.

**Verificar instalación:**
```bash
python -c "import sqlite3; print('SQLite:', sqlite3.sqlite_version)"
```

### 2. Primer Uso

La base de datos se crea automáticamente en la primera ejecución:

```bash
python job_search.py
```

**Output esperado:**
```
==================================================
🤖 PulseBot - Buscador de Empleos Inteligente
==================================================
🗄️ Inicializando base de datos...
✅ Base de datos inicializada
📊 Ofertas procesadas anteriormente: 0
```

### 3. Ejecuciones Subsecuentes

El bot automáticamente:
1. ✅ Verifica la DB antes de buscar
2. ✅ Filtra ofertas ya procesadas
3. ✅ Clasifica nuevas ofertas
4. ✅ Detecta LatAm matches
5. ✅ Guarda en DB con metadatos

---

## 🔧 Personalización

### Agregar Categorías Nuevas

Edita el diccionario `CATEGORIES` en [job_search.py](job_search.py#L30):

```python
CATEGORIES = {
    '🚀 STARTUP': [...],
    '🏢 FACTORY/STAFFING': [...],
    '💳 FINTECH/AI': [...],
    '🎮 GAMING': [  # Nueva categoría
        'game development', 'unity', 'unreal engine',
        'mobile gaming', 'esports'
    ]
}
```

### Agregar Keywords de LatAm

Edita la lista `LATAM_KEYWORDS`:

```python
LATAM_KEYWORDS = [
    'timezone alignment', 'gmt-3', 'gmt-5',
    # ... keywords existentes ...
    'buenos aires time',  # Nueva keyword
    'santiago timezone'   # Nueva keyword
]
```

### Agregar Nichos

Edita la función `detect_niche()`:

```python
niches = {
    'SaaS': [...],
    'Fintech': [...],
    'Cyber Security': [  # Nuevo nicho
        'cybersecurity', 'infosec', 'penetration testing',
        'security engineer', 'ethical hacking'
    ]
}
```

---

## 📈 Ventajas del Nuevo Sistema

### Antes (Sistema Antiguo):
- ❌ Todas las ofertas se veían iguales
- ❌ No se distinguía tipo de empresa
- ❌ Difícil identificar ofertas relevantes para LatAm
- ❌ Archivo JSON limitado
- ❌ Sin metadatos enriquecidos

### Ahora (Sistema Mejorado):
- ✅ Clasificación automática en 4 categorías
- ✅ Detección de 7+ nichos tecnológicos
- ✅ Identificación clara de ofertas LatAm con 🔥
- ✅ Base de datos SQLite robusta
- ✅ Metadatos enriquecidos (categoría, LatAm match, timestamp)
- ✅ Análisis histórico posible
- ✅ Escalable a miles de ofertas
- ✅ ID único para cada oferta

---

## 🎯 Casos de Uso

### 1. Filtrar solo Startups con LatAm Match

Las ofertas más relevantes aparecen con:
```
🔥 [🚀 STARTUP] ...
```

### 2. Evitar Factories/Staffing

Si ves:
```
[🏢 FACTORY/STAFFING] ...
```
Puedes saltarte fácilmente si no te interesan consultorías.

### 3. Buscar nichos específicos

```
💰 Nicho: Fintech
```
Te ayuda a identificar ofertas en tu área de interés.

### 4. Verificar ofertas previamente enviadas

Usando el ID puedes buscar en la DB:
```python
import sqlite3
conn = sqlite3.connect('processed_jobs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM processed_jobs WHERE job_id LIKE 'a1b2c3d4e5f6%'")
print(cursor.fetchone())
```

---

## 🐛 Troubleshooting

### Error: "table processed_jobs already exists"

**Causa:** La DB ya está inicializada.

**Solución:** No hay problema, el código maneja esto automáticamente con `CREATE TABLE IF NOT EXISTS`.

### No se detectan categorías

**Causa:** Las keywords no están presentes en título o descripción.

**Solución:** 
1. Verifica las keywords en `CATEGORIES`
2. Considera agregar sinónimos o variaciones
3. La oferta se marcará como `📋 GENERAL`

### No se detecta LatAm Match

**Causa:** La oferta no menciona keywords de LatAm.

**Solución:** Es esperado. Solo aparece 🔥 si la oferta menciona explícitamente LatAm, timezones, o español.

### DB se corrompe

**Solución rápida:**
```bash
# Respaldar
cp processed_jobs.db processed_jobs.db.backup

# Recrear
rm processed_jobs.db
python job_search.py
```

---

## 📚 Referencias

### Archivos Modificados:
- [job_search.py](job_search.py) - Lógica principal (líneas 1-1013)

### Nuevas Funciones:
- `init_database()` - Inicializa SQLite
- `is_job_processed(job_id)` - Verifica si oferta fue procesada
- `save_processed_job(...)` - Guarda con metadatos
- `get_processed_count()` - Total en DB
- `classify_job(job)` - Clasifica en categorías
- `is_latam_match(job)` - Detecta LatAm keywords
- `detect_niche(job)` - Detecta nicho tecnológico

### Funciones Modificadas:
- `format_job_message()` - Nuevo formato con categoría, nicho, LatAm match, ID
- `send_to_telegram()` - Guarda en DB automáticamente
- `filter_new_jobs()` - Usa SQLite en lugar de Set
- `main()` - Inicializa DB, muestra estadísticas

---

## ✅ Checklist de Testing

- [ ] ✅ Base de datos se crea automáticamente
- [ ] ✅ Ofertas se clasifican correctamente
- [ ] ✅ Emoji 🔥 aparece solo en LatAm matches
- [ ] ✅ Nichos se detectan correctamente
- [ ] ✅ IDs son únicos y consistentes
- [ ] ✅ No se envían duplicados (verificación en DB)
- [ ] ✅ Estadísticas se muestran correctamente
- [ ] ✅ Mensajes en Telegram tienen nuevo formato
- [ ] ✅ DB persiste entre ejecuciones
- [ ] ✅ Performance adecuado (SQLite es rápido)

---

## 🚀 Próximos Pasos

### Mejoras Futuras Sugeridas:

1. **Dashboard de Estadísticas**
   - Gráficas de distribución por categoría
   - Tendencias de LatAm matches
   - Nichos más populares

2. **Filtros Personalizables**
   - Configurar categorías favoritas
   - Excluir categorías no deseadas
   - Priorizar LatAm matches

3. **Machine Learning**
   - Clasificación más precisa con ML
   - Predicción de salario basado en histórico
   - Detección de red flags

4. **Notificaciones Priorizadas**
   - Alertas inmediatas para 🔥 matches
   - Resumen diario de categorías
   - Emails para ofertas premium

---

**Última actualización:** Diciembre 20, 2025  
**Versión:** 2.0.0  
**Autor:** PulseBot Team
