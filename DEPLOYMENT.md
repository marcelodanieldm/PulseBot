# 🚀 Guía de Despliegue en GitHub Actions

## 📋 Configuración del Despliegue Automático

PulseBot puede ejecutarse automáticamente cada 6 horas en GitHub Actions de forma **100% gratuita**.

---

## ⚙️ Paso 1: Configurar GitHub Secrets

Las credenciales deben guardarse como **Secrets** en GitHub para mantenerlas seguras.

### 1. Ve a tu repositorio en GitHub

```
https://github.com/TU_USUARIO/PulseBot
```

### 2. Navega a Settings > Secrets and variables > Actions

```
Repositorio → Settings → (lado izquierdo) Secrets and variables → Actions
```

### 3. Haz clic en "New repository secret"

### 4. Añade estos 3 secrets:

#### Secret 1: RAPIDAPI_KEY
- **Name**: `RAPIDAPI_KEY`
- **Secret**: Tu API key de RapidAPI (JSearch)
- Ejemplo: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

#### Secret 2: TELEGRAM_BOT_TOKEN
- **Name**: `TELEGRAM_BOT_TOKEN`
- **Secret**: Token de tu bot de Telegram
- Ejemplo: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

#### Secret 3: TELEGRAM_CHAT_ID
- **Name**: `TELEGRAM_CHAT_ID`
- **Secret**: Tu Chat ID de Telegram
- Ejemplo: `987654321` o `-1001234567890` (para grupos/canales)

✅ **Verificación**: Deberías tener 3 secrets configurados:
- ✓ RAPIDAPI_KEY
- ✓ TELEGRAM_BOT_TOKEN
- ✓ TELEGRAM_CHAT_ID

---

## 📅 Paso 2: Verificar el Workflow

El archivo [.github/workflows/main.yml](.github/workflows/main.yml) ya está configurado con:

### ⏰ Programación Automática
```yaml
schedule:
  - cron: '0 */6 * * *'  # Cada 6 horas
```

**Horarios de ejecución (UTC):**
- 00:00 UTC (9:00 PM hora del Este de EE.UU., día anterior)
- 06:00 UTC (3:00 AM hora del Este de EE.UU.)
- 12:00 UTC (9:00 AM hora del Este de EE.UU.)
- 18:00 UTC (3:00 PM hora del Este de EE.UU.)

**Para ajustar el horario:**
- Cada 3 horas: `'0 */3 * * *'`
- Cada 12 horas: `'0 */12 * * *'`
- Cada día a las 9 AM UTC: `'0 9 * * *'`
- Usa [crontab.guru](https://crontab.guru/) para crear tu horario

### 🔄 Ejecución Manual
Puedes ejecutar el bot manualmente desde:
```
Actions → PulseBot Job Search → Run workflow
```

### 🚫 Sistema Anti-Duplicados
- Archivo `sent_jobs.json` registra ofertas enviadas
- Se actualiza automáticamente después de cada ejecución
- Se versionan los cambios en git
- **No se enviarán ofertas repetidas**

---

## 🎯 Paso 3: Hacer Push y Activar

### 1. Commit y push de los cambios

```bash
git add .
git commit -m "🚀 Deploy: Configuración de GitHub Actions para ejecución automática

- Workflow configurado para ejecutarse cada 6 horas
- Sistema anti-duplicados con sent_jobs.json
- Integración con GitHub Secrets
- Ejecución manual disponible"

git push origin main
```

### 2. Verificar en GitHub

Ve a la pestaña **Actions** en tu repositorio:
```
https://github.com/TU_USUARIO/PulseBot/actions
```

✅ Deberías ver el workflow "PulseBot Job Search"

### 3. Ejecutar manualmente (opcional)

Para probar inmediatamente:
1. Ve a **Actions** → **PulseBot Job Search**
2. Click en **Run workflow**
3. Selecciona la rama `main`
4. Click en **Run workflow** (botón verde)

---

## 📊 Paso 4: Monitorear Ejecuciones

### Ver logs en tiempo real

1. Ve a **Actions**
2. Click en la ejecución más reciente
3. Click en el job "search-jobs"
4. Verás los logs completos

### Qué esperar en los logs

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
✅ Encontrados X trabajos en página 1
...

📤 Enviando 5 ofertas a Telegram...
[1/5] Enviando: Senior Software Engineer - TechCorp
  🔍 Analizando reputación de TechCorp...
  ✅ Enviado correctamente
...

💾 Historial actualizado: 5 ofertas registradas
✨ Proceso completado: 5/5 ofertas enviadas
📊 Total histórico: 5 ofertas enviadas
```

### Verificar en Telegram

Abre tu chat/canal de Telegram y verifica que recibiste las ofertas.

---

## 🔧 Personalización

### Cambiar frecuencia de ejecución

Edita [.github/workflows/main.yml](.github/workflows/main.yml):

```yaml
schedule:
  - cron: '0 */3 * * *'  # Cambiar a cada 3 horas
```

### Cambiar criterios de búsqueda

Edita [job_search.py](job_search.py) línea ~340:

```python
jobs = search_jobs(
    query="Python Developer startup",  # Cambiar búsqueda
    location="Argentina",               # Cambiar ubicación
    remote_jobs_only=True,
    num_pages=3                        # Más páginas
)
```

Después de cambiar:
```bash
git add job_search.py
git commit -m "🔧 Update: Criterios de búsqueda personalizados"
git push origin main
```

---

## 🛠️ Troubleshooting

### ❌ Error: "RAPIDAPI_KEY no configurada"
**Solución:**
1. Ve a Settings → Secrets and variables → Actions
2. Verifica que `RAPIDAPI_KEY` esté configurado
3. El nombre debe ser exactamente `RAPIDAPI_KEY` (mayúsculas)
4. Re-ejecuta el workflow

### ❌ Error: "Credenciales de Telegram no configuradas"
**Solución:**
1. Verifica que ambos secrets existan:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
2. Los nombres deben ser exactos (mayúsculas)
3. El Chat ID puede ser negativo (normal para grupos/canales)

### ❌ El workflow no se ejecuta automáticamente
**Posibles causas:**
1. **Primera ejecución**: El cron job puede tardar hasta 1 hora en activarse la primera vez
2. **Repositorio privado**: Asegúrate de que Actions esté habilitado en Settings → Actions
3. **Límites de GitHub**: El plan gratuito tiene 2000 minutos/mes (suficiente para PulseBot)

**Solución temporal**: Ejecuta manualmente desde Actions → Run workflow

### ❌ No se reciben ofertas
**Causas normales:**
1. ✅ **Todas las ofertas ya fueron enviadas** (el sistema anti-duplicados está funcionando)
2. ✅ **No hay ofertas nuevas** que coincidan con los criterios
3. ✅ **La API no tiene resultados** para esos filtros específicos

**Para verificar:**
- Revisa los logs en Actions
- Busca el mensaje: "No hay nuevas ofertas. Todas las ofertas encontradas ya fueron enviadas anteriormente."
- Esto es normal y esperado

### 📊 Ver historial de ofertas enviadas

El archivo `sent_jobs.json` contiene el registro:

```json
{
  "sent_job_ids": [
    "a1b2c3d4e5f6g7h8i9j0",
    "1a2b3c4d5e6f7g8h9i0j"
  ],
  "last_updated": "2025-12-20 15:30:00 UTC"
}
```

Cada hash MD5 representa una oferta única.

---

## 💡 Ventajas del Despliegue en GitHub Actions

✅ **100% Gratuito**
- 2000 minutos/mes en plan gratuito
- PulseBot usa ~2 minutos por ejecución
- = ~1000 ejecuciones/mes posibles
- = Ejecutar cada 6 horas está muy por debajo del límite

✅ **Automatizado**
- Se ejecuta sin intervención manual
- Cron job confiable
- No necesitas servidor propio

✅ **Seguro**
- Credenciales en GitHub Secrets (encriptadas)
- No se exponen en el código
- Logs públicos no muestran secrets

✅ **Anti-Duplicados**
- Sistema de tracking automático
- No recibes ofertas repetidas
- Historial versionado en git

✅ **Monitoreable**
- Logs detallados de cada ejecución
- Notificaciones de errores por email (opcional)
- Summary de cada ejecución

✅ **Escalable**
- Fácil de modificar criterios
- Fácil de cambiar frecuencia
- Fácil de añadir más funcionalidades

---

## 📈 Estimación de Uso

**Por ejecución:**
- Tiempo: ~2 minutos
- Ofertas enviadas: 0-5 (solo nuevas)
- API calls: 2-3 (JSearch + DuckDuckGo)

**Por día (4 ejecuciones):**
- Tiempo total: ~8 minutos
- Ofertas: 0-20 (depende de disponibilidad)
- Bajo el límite de GitHub (2000 min/mes)

**Por mes:**
- Tiempo total: ~240 minutos (~12% del límite gratuito)
- Ofertas: Potencialmente cientos
- Costo: $0 🎉

---

## 🎉 ¡Todo Listo!

Tu bot ahora:
- ✅ Se ejecuta automáticamente cada 6 horas
- ✅ Busca ofertas de empleo
- ✅ Analiza reputación de empresas
- ✅ Envía alertas a Telegram
- ✅ No envía duplicados
- ✅ Funciona 24/7 en la nube
- ✅ Completamente gratis

**Próximos pasos:**
1. Espera la primera ejecución automática (máximo 6 horas)
2. O ejecuta manualmente desde Actions
3. Revisa tus ofertas en Telegram
4. ¡Empieza a aplicar! 🚀

---

## 📞 Soporte Adicional

- 📖 [README.md](README.md) - Documentación general
- ⚡ [QUICKSTART.md](QUICKSTART.md) - Inicio rápido local
- ✅ [CHECKLIST.md](CHECKLIST.md) - Checklist de configuración
- 🔧 [GitHub Actions Docs](https://docs.github.com/en/actions) - Documentación oficial

---

```
╔════════════════════════════════════════════════════════╗
║                                                        ║
║   🚀 PulseBot desplegado en GitHub Actions 🚀         ║
║                                                        ║
║   ⏰ Automático • 🔒 Seguro • 🆓 Gratis • 🚫 Sin Spam ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```
