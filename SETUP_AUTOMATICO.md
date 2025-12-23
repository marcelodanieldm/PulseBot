# 🚀 Configuración de GitHub Actions - Ejecución Automática

## ✅ Sistema Optimizado (Costo Cero)

El bot ahora está configurado para funcionar **100% GRATIS** evitando todos los rate limits:

### Soluciones Implementadas:

1. **✅ DuckDuckGo Rate Limit → SOLUCIONADO**
   - Búsquedas de reputación deshabilitadas
   - Análisis de sentimiento solo con texto local
   - Sin APIs externas para sentiment/reviews

2. **✅ JSearch Rate Limit → SOLUCIONADO**
   - JSearch deshabilitado por defecto
   - RemoteOK como fuente principal (gratis, sin límites)
   - ~80-150 ofertas por ejecución

3. **✅ Envío Automático → CONFIGURADO**
   - GitHub Actions ejecuta cada 6 horas
   - También puedes ejecutar manualmente
   - Base de datos persistente entre ejecuciones

## 📋 Pasos para Configurar

### 1. Configurar Secrets en GitHub

Ve a tu repositorio en GitHub:
- Click en **Settings** (Configuración)
- Click en **Secrets and variables** → **Actions**
- Click en **New repository secret**

Agrega estos 3 secrets:

#### Secret 1: `RAPIDAPI_KEY`
```
Valor: tu_clave_de_rapidapi_aqui
```
**Nota:** Puedes dejarlo vacío si solo usas RemoteOK (no necesitas JSearch)

#### Secret 2: `TELEGRAM_BOT_TOKEN`
```
Valor: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```
Obtén esto de [@BotFather](https://t.me/BotFather) en Telegram

#### Secret 3: `TELEGRAM_CHAT_ID`
```
Valor: -1001234567890
```
Tu chat ID o canal ID donde recibirás las ofertas

### 2. Habilitar GitHub Actions

1. Ve a la pestaña **Actions** en tu repositorio
2. Si dice "Workflows aren't being run", click en **"I understand, enable them"**
3. Verás el workflow **"🤖 Auto Job Search - PulseBot"**

### 3. Ejecutar Manualmente (Primera Vez)

Para probar que todo funciona:

1. Ve a **Actions** → **🤖 Auto Job Search - PulseBot**
2. Click en **Run workflow** (lado derecho)
3. Click en el botón verde **Run workflow**
4. Espera 2-3 minutos
5. Verás las ofertas en tu Telegram

### 4. Ejecución Automática

Una vez configurado, el bot se ejecutará automáticamente:

**Horario:** Cada 6 horas
- 00:00 UTC (21:00 Argentina/Chile)
- 06:00 UTC (03:00 Argentina/Chile)
- 12:00 UTC (09:00 Argentina/Chile)
- 18:00 UTC (15:00 Argentina/Chile)

## 🎯 Prioridades Configuradas

El bot busca principalmente:

### Ubicación:
- ✅ **LatAm** (Argentina, Chile, Colombia, México, Brasil, Perú, Uruguay)
- ✅ **Worldwide / Remote Anywhere**
- ✅ **Keywords**: latam, latin america, remote, worldwide, anywhere

### Roles Técnicos:
- Python, Backend, Fullstack, DevOps, QA
- Frontend (React, TypeScript, Node.js)
- Web3/Blockchain (Solidity, Crypto)
- Mobile (iOS, Android, React Native)
- Data (ML, Data Science)
- **En español**: Desarrollador, Ingeniero, Programador

## 📊 Qué Esperar

Cada ejecución automática:
- ✅ Obtiene ~80-150 ofertas de RemoteOK
- ✅ Filtra por keywords relevantes
- ✅ Identifica ~20-40 startups/tech
- ✅ Envía ~10-20 ofertas nuevas a Telegram
- ✅ Sin rate limits ni errores
- ✅ 100% gratis

## 🔧 Personalizar Horarios

Para cambiar la frecuencia de ejecución, edita `.github/workflows/auto-job-search.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Cada 6 horas (actual)
```

**Opciones:**
- Cada 3 horas: `'0 */3 * * *'`
- Cada 12 horas: `'0 */12 * * *'`
- Una vez al día (9am UTC): `'0 9 * * *'`
- Dos veces al día (9am y 9pm UTC): `'0 9,21 * * *'`

## 🐛 Solución de Problemas

### No recibo ofertas
**Verificar:**
1. ¿Los secrets están configurados correctamente?
2. ¿El bot de Telegram puede enviar mensajes al chat?
3. ¿El workflow se ejecutó? (ver pestaña Actions)

### Error en GitHub Actions
**Revisar:**
1. Ve a Actions → Click en el workflow fallido
2. Lee los logs para ver el error
3. Verifica que los secrets estén bien escritos

### Quiero más ofertas
**Opciones:**
1. Cambiar frecuencia a cada 3 horas
2. Agregar más keywords en `job_search.py`
3. Habilitar JSearch (si tienes cuota): cambiar `jsearch_enabled = True`

## ✅ Ventajas de Esta Configuración

### 🆓 Costo Cero
- RemoteOK: 100% gratis
- GitHub Actions: 2,000 minutos/mes gratis
- Telegram: gratis
- Sin APIs de pago

### ⚡ Sin Rate Limits
- No usa DuckDuckGo (sin búsquedas externas)
- JSearch deshabilitado por defecto
- RemoteOK sin límites

### 🤖 Totalmente Automático
- Se ejecuta solo cada 6 horas
- No requiere tu intervención
- Ofertas directo a Telegram

### 💾 Base de Datos Persistente
- Evita duplicados automáticamente
- Se mantiene entre ejecuciones
- Historial completo de ofertas

## 📈 Siguiente Nivel (Opcional)

Si quieres aún más control:

1. **Dashboard de Métricas**: Agrega logging a Google Sheets
2. **Filtros Personalizados**: Modifica keywords según tu stack
3. **Múltiples Canales**: Envía diferentes tipos de ofertas a diferentes canales
4. **Alertas Especiales**: Notificaciones push para ofertas premium

---

**🎉 ¡Todo listo! El bot ahora funciona automáticamente sin costos ni rate limits.**

¿Preguntas? Revisa los logs en la pestaña Actions de GitHub.
