"""
PulseBot - Job Search Script
Busca ofertas de empleo usando JSearch API y las envía a Telegram
Incluye Reputation Check para evaluar empresas
"""

import os
import requests
import time
import re
import json
import hashlib
from typing import List, Dict, Optional, Tuple, Set
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from textblob import TextBlob
from bs4 import BeautifulSoup

# Cargar variables de entorno
load_dotenv()

# Configuración
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Plataformas ATS permitidas
ALLOWED_PLATFORMS = ['greenhouse.io', 'lever.co', 'bamboohr.com']

# Archivo para tracking de ofertas enviadas
SENT_JOBS_FILE = 'sent_jobs.json'


def load_sent_jobs() -> Set[str]:
    """
    Carga el registro de ofertas ya enviadas
    
    Returns:
        Set con IDs de ofertas ya enviadas
    """
    if os.path.exists(SENT_JOBS_FILE):
        try:
            with open(SENT_JOBS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                sent_ids = data.get('sent_job_ids', [])
                print(f"✅ Historial cargado: {len(sent_ids)} ofertas registradas")
                return set(sent_ids)
        except json.JSONDecodeError as e:
            print(f"⚠️ Error decodificando JSON: {e}. Creando historial nuevo.")
            return set()
        except IOError as e:
            print(f"⚠️ Error leyendo archivo: {e}")
            return set()
        except Exception as e:
            print(f"⚠️ Error inesperado cargando historial: {e}")
            return set()
    else:
        print("📝 No existe historial previo, creando nuevo")
    return set()


def save_sent_jobs(sent_ids: Set[str]):
    """
    Guarda el registro de ofertas enviadas
    
    Args:
        sent_ids: Set con IDs de ofertas enviadas
    """
    try:
        data = {
            'sent_job_ids': list(sent_ids),
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
            'total_sent': len(sent_ids)
        }
        with open(SENT_JOBS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Historial actualizado: {len(sent_ids)} ofertas registradas")
    except IOError as e:
        print(f"❌ Error de I/O guardando historial: {e}")
        print("⚠️ El historial no se guardó, pero el bot continuará funcionando")
    except TypeError as e:
        print(f"❌ Error de tipo al serializar datos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado guardando historial: {e}")
        print("⚠️ El historial no se guardó, pero el bot continuará funcionando")


def generate_job_id(job: Dict) -> str:
    """
    Genera un ID único para una oferta de empleo
    
    Args:
        job: Diccionario con datos del trabajo
    
    Returns:
        ID único (hash MD5)
    """
    try:
        # Usar múltiples campos para generar un ID único
        job_apply_link = job.get('job_apply_link', '')
        
        # Si hay link de aplicación, usarlo como base
        if job_apply_link:
            unique_string = job_apply_link
        else:
            # Fallback: combinar título, empresa y ubicación
            title = job.get('job_title', '')
            company = job.get('employer_name', '')
            location = job.get('job_city', '') + job.get('job_country', '')
            unique_string = f"{title}|{company}|{location}"
        
        # Generar hash MD5
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"⚠️ Error generando ID único: {e}")
        # Fallback: generar ID basado en timestamp
        return hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()


def filter_new_jobs(jobs: List[Dict], sent_ids: Set[str]) -> List[Dict]:
    """
    Filtra trabajos que ya fueron enviados
    
    Args:
        jobs: Lista de ofertas de empleo
        sent_ids: Set con IDs de ofertas ya enviadas
    
    Returns:
        Lista de ofertas nuevas (no enviadas)
    """
    new_jobs = []
    
    try:
        for job in jobs:
            try:
                job_id = generate_job_id(job)
                if job_id not in sent_ids:
                    new_jobs.append(job)
            except Exception as e:
                print(f"⚠️ Error procesando trabajo individual: {e}")
                # Continuar con el siguiente trabajo
                continue
        
        duplicates = len(jobs) - len(new_jobs)
        if duplicates > 0:
            print(f"🔄 Filtrados {duplicates} trabajos duplicados")
        
        return new_jobs
    except Exception as e:
        print(f"❌ Error inesperado en filtrado: {e}")
        print("⚠️ Devolviendo todos los trabajos sin filtrar")
        return jobs


def search_jobs(query: str = "Software Engineer", 
                location: str = "Latin America", 
                remote_jobs_only: bool = True,
                num_pages: int = 1) -> List[Dict]:
    """
    Busca ofertas de empleo usando la API de JSearch
    
    Args:
        query: Término de búsqueda (ej: "Software Engineer")
        location: Ubicación (ej: "Latin America")
        remote_jobs_only: Si buscar solo trabajos remotos
        num_pages: Número de páginas a buscar
    
    Returns:
        Lista de ofertas de empleo
    """
    url = f"https://{RAPIDAPI_HOST}/search"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    all_jobs = []
    
    for page in range(1, num_pages + 1):
        querystring = {
            "query": f"{query} {location}",
            "page": str(page),
            "num_pages": "1",
            "date_posted": "week"  # Solo trabajos de la última semana
        }
        
        if remote_jobs_only:
            querystring["remote_jobs_only"] = "true"
        
        try:
            print(f"🔍 Buscando página {page}...")
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('data', [])
            
            if jobs:
                all_jobs.extend(jobs)
                print(f"✅ Encontrados {len(jobs)} trabajos en página {page}")
            else:
                print(f"⚠️ No se encontraron trabajos en página {page}")
            
            # Pequeña pausa para no saturar la API
            time.sleep(1)
            
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout en página {page}. Continuando con la siguiente...")
            continue
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error HTTP en página {page}: {e}")
            if e.response.status_code == 429:
                print("⚠️ Rate limit alcanzado. Esperando 5 segundos...")
                time.sleep(5)
                continue
            elif e.response.status_code >= 500:
                print("⚠️ Error del servidor. Continuando con lo obtenido...")
                break
            else:
                break
        except requests.exceptions.ConnectionError:
            print(f"❌ Error de conexión en página {page}. Verificando conectividad...")
            break
        except requests.exceptions.RequestException as e:
            print(f"❌ Error inesperado al buscar trabajos en página {page}: {e}")
            break
        except json.JSONDecodeError:
            print(f"❌ Error decodificando respuesta JSON en página {page}")
            continue
        except Exception as e:
            print(f"❌ Error inesperado en búsqueda: {e}")
            break
    
    if not all_jobs:
        print("⚠️ No se encontraron trabajos en ninguna página")
    
    return all_jobs


def filter_jobs_by_platform(jobs: List[Dict]) -> List[Dict]:
    """
    Filtra trabajos que usen plataformas ATS específicas
    
    Args:
        jobs: Lista de ofertas de empleo
    
    Returns:
        Lista filtrada de ofertas
    """
    filtered_jobs = []
    
    try:
        for job in jobs:
            try:
                job_apply_link = job.get('job_apply_link', '')
                
                # Verificar si el link contiene alguna de las plataformas permitidas
                if job_apply_link and any(platform in job_apply_link.lower() for platform in ALLOWED_PLATFORMS):
                    filtered_jobs.append(job)
            except AttributeError as e:
                print(f"⚠️ Error procesando link de trabajo: {e}")
                continue
            except Exception as e:
                print(f"⚠️ Error inesperado procesando trabajo: {e}")
                continue
        
        print(f"📊 Filtrados {len(filtered_jobs)} de {len(jobs)} trabajos por plataforma ATS")
        return filtered_jobs
    except Exception as e:
        print(f"❌ Error crítico en filtrado por plataforma: {e}")
        print("⚠️ Devolviendo lista vacía para evitar fallos")
        return []
    
    print(f"📊 Filtrados {len(filtered_jobs)} de {len(jobs)} trabajos por plataforma ATS")
    return filtered_jobs


def filter_startup_jobs(jobs: List[Dict]) -> List[Dict]:
    """
    Intenta filtrar trabajos de startups basándose en indicadores
    
    Args:
        jobs: Lista de ofertas de empleo
    
    Returns:
        Lista filtrada de ofertas
    """
    startup_keywords = ['startup', 'early stage', 'seed', 'series a', 'series b', 
                        'fast-growing', 'scale-up', 'venture', 'funded']
    
    filtered_jobs = []
    
    for job in jobs:
        job_description = (job.get('job_description', '') or '').lower()
        employer_name = (job.get('employer_name', '') or '').lower()
        
        # Buscar palabras clave relacionadas con startups
        if any(keyword in job_description or keyword in employer_name 
               for keyword in startup_keywords):
            filtered_jobs.append(job)
        else:
            # Si no hay descripción completa, incluir el trabajo de todos modos
            # para no perder oportunidades
            if not job_description:
                filtered_jobs.append(job)
    
    # Si el filtro es muy restrictivo, devolver todos los trabajos
    if len(filtered_jobs) < 5:
        print("⚠️ Filtro de startup muy restrictivo, devolviendo todos los trabajos")
        return jobs
    
    print(f"🚀 Filtrados {len(filtered_jobs)} trabajos potenciales de startups")
    return filtered_jobs


def search_company_reviews(company_name: str) -> Optional[str]:
    """
    Busca reviews de empleados en DuckDuckGo
    
    Args:
        company_name: Nombre de la empresa
    
    Returns:
        Snippet del resultado o None
    """
    if not company_name:
        return None
        
    try:
        query = f"{company_name} employee reviews glassdoor"
        
        # Intentar con delays más largos para evitar rate limiting
        time.sleep(2)  # Pausa antes de la búsqueda
        
        with DDGS() as ddgs:
            try:
                results = list(ddgs.text(query, max_results=3))
            except Exception as search_error:
                print(f"  ⚠️ Error en búsqueda DuckDuckGo: {search_error}")
                return None
            
            if results:
                # Buscar resultados relevantes (Glassdoor, Indeed, etc.)
                for result in results:
                    try:
                        title = result.get('title', '').lower()
                        body = result.get('body', '')
                        
                        if any(site in title for site in ['glassdoor', 'indeed', 'comparably']):
                            # Intentar extraer rating del snippet
                            snippet = body[:200] + "..." if len(body) > 200 else body
                            return snippet
                    except Exception as e:
                        print(f"  ⚠️ Error procesando resultado: {e}")
                        continue
                
                # Si no hay resultados específicos, retornar el primero
                try:
                    first_result = results[0].get('body', '')
                    return first_result[:200] + "..." if first_result else None
                except Exception:
                    return None
        
        return None
    except ImportError:
        print(f"  ⚠️ DuckDuckGo search no disponible. Instala: pip install duckduckgo-search")
        return None
    except Exception as e:
        # Si hay rate limiting, no es crítico - continuar sin reviews
        error_msg = str(e).lower()
        if "ratelimit" in error_msg or "rate limit" in error_msg:
            print(f"  ⏳ Rate limit alcanzado, continuando sin reviews...")
        else:
            print(f"  ⚠️ Error buscando reviews para {company_name}: {e}")
        return None


def analyze_company_sentiment(company_name: str, job_description: str) -> str:
    """
    Analiza el sentimiento de la descripción de la empresa
    
    Args:
        company_name: Nombre de la empresa
        job_description: Descripción del trabajo
    
    Returns:
        'Positivo', 'Neutral' o 'Negativo'
    """
    try:
        if not job_description:
            return "Neutral"
        
        # Tomar solo los primeros 500 caracteres para el análisis
        text_sample = job_description[:500]
        
        try:
            blob = TextBlob(text_sample)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return "Positivo"
            elif polarity < -0.1:
                return "Negativo"
            else:
                return "Neutral"
        except Exception as analysis_error:
            print(f"  ⚠️ Error en análisis de polaridad: {analysis_error}")
            return "Neutral"
            
    except ImportError:
        print(f"  ⚠️ TextBlob no disponible. Instala: pip install textblob")
        return "Neutral"
    except Exception as e:
        print(f"  ⚠️ Error analizando sentimiento para {company_name}: {e}")
        return "Neutral"


def count_company_active_jobs(company_name: str, all_jobs: List[Dict]) -> int:
    """
    Cuenta cuántas vacantes activas tiene la empresa en la lista de trabajos
    
    Args:
        company_name: Nombre de la empresa
        all_jobs: Lista de todos los trabajos encontrados
    
    Returns:
        Número de vacantes activas
    """
    if not company_name or not all_jobs:
        return 0
        
    try:
        count = 0
        company_lower = company_name.lower().strip()
        
        for job in all_jobs:
            try:
                employer = (job.get('employer_name', '') or '').lower().strip()
                if employer == company_lower:
                    count += 1
            except AttributeError:
                continue
            except Exception as e:
                print(f"  ⚠️ Error procesando trabajo en conteo: {e}")
                continue
        
        return count
    except Exception as e:
        print(f"  ⚠️ Error contando vacantes: {e}")
        return 1  # Al menos la vacante actual


def calculate_hiring_probability(active_jobs: int, has_reviews: bool, sentiment: str) -> Tuple[str, str]:
    """
    Calcula la probabilidad de contratación basada en varios factores
    
    Args:
        active_jobs: Número de vacantes activas
        has_reviews: Si se encontraron reviews
        sentiment: Sentimiento de la descripción
    
    Returns:
        Tupla (nivel, emoji) donde nivel es 'Alta', 'Media' o 'Baja'
    """
    score = 0
    
    # Factor 1: Número de vacantes activas (más importante)
    if active_jobs >= 5:
        score += 3
    elif active_jobs >= 3:
        score += 2
    elif active_jobs >= 2:
        score += 1
    
    # Factor 2: Presencia en sitios de reviews (indica empresa establecida)
    if has_reviews:
        score += 1
    
    # Factor 3: Sentimiento positivo
    if sentiment == "Positivo":
        score += 1
    elif sentiment == "Negativo":
        score -= 1
    
    # Clasificar
    if score >= 4:
        return "Alta", "🔥"
    elif score >= 2:
        return "Media", "⚡"
    else:
        return "Baja", "💤"


def format_job_message(job: Dict, all_jobs: List[Dict] = None) -> str:
    """
    Formatea la información del trabajo para Telegram
    
    Args:
        job: Diccionario con datos del trabajo
        all_jobs: Lista de todos los trabajos (para contar vacantes activas)
    
    Returns:
        Mensaje formateado o None si hay error crítico
    """
    try:
        title = job.get('job_title', 'N/A')
        company = job.get('employer_name', 'N/A')
        location = job.get('job_city', 'Remote')
        country = job.get('job_country', '')
        
        if country:
            location = f"{location}, {country}"
        
        apply_link = job.get('job_apply_link', 'N/A')
        
        # Información salarial con manejo seguro
        try:
            salary_min = job.get('job_min_salary')
            salary_max = job.get('job_max_salary')
            salary_currency = job.get('job_salary_currency', 'USD')
            
            if salary_min and salary_max:
                salary = f"💰 ${salary_min:,.0f} - ${salary_max:,.0f} {salary_currency}"
            elif salary_min:
                salary = f"💰 Desde ${salary_min:,.0f} {salary_currency}"
            elif salary_max:
                salary = f"💰 Hasta ${salary_max:,.0f} {salary_currency}"
            else:
                salary = "💰 Salario no especificado"
        except (ValueError, TypeError):
            salary = "💰 Salario no especificado"
        
        # Detectar plataforma ATS
        platform = "Otra"
        try:
            for p in ALLOWED_PLATFORMS:
                if apply_link and p in apply_link.lower():
                    platform = p.replace('.io', '').replace('.co', '').replace('.com', '').title()
                    break
        except AttributeError:
            platform = "Otra"
        
        # === REPUTATION CHECK ===
        print(f"  🔍 Analizando reputación de {company}...")
        
        # 1. Buscar reviews (con protección)
        reviews_snippet = None
        has_reviews = False
        try:
            reviews_snippet = search_company_reviews(company)
            has_reviews = reviews_snippet is not None
        except Exception as e:
            print(f"  ⚠️ Error obteniendo reviews: {e}")
        
        # 2. Analizar sentimiento (con protección)
        sentiment = "Neutral"
        try:
            job_description = job.get('job_description', '')
            sentiment = analyze_company_sentiment(company, job_description)
        except Exception as e:
            print(f"  ⚠️ Error en análisis de sentimiento: {e}")
        
        # 3. Contar vacantes activas (con protección)
        active_jobs = 1  # Al menos esta vacante
        try:
            if all_jobs:
                active_jobs = count_company_active_jobs(company, all_jobs)
        except Exception as e:
            print(f"  ⚠️ Error contando vacantes: {e}")
# 4. Calcular probabilidad de contratación (con protección)
        probability = "Media"
        emoji = "⚡"
        try:
            probability, emoji = calculate_hiring_probability(active_jobs, has_reviews, sentiment)
        except Exception as e:
            print(f"  ⚠️ Error calculando probabilidad: {e}")
        
        # Construir sección de análisis
        analysis_section = f"\n📊 <b>Análisis de Empresa:</b>\n"
        analysis_section += f"   • Vacantes activas: {active_jobs}\n"
        analysis_section += f"   • Sentimiento: {sentiment}\n"
        
        if reviews_snippet:
            try:
                # Limpiar y acortar snippet
                clean_snippet = reviews_snippet.replace('<', '').replace('>', '').strip()
                if len(clean_snippet) > 150:
                    clean_snippet = clean_snippet[:150] + "..."
                analysis_section += f"   • Review: \"{clean_snippet}\"\n"
            except Exception as e:
                print(f"  ⚠️ Error procesando review snippet: {e}")
        
        analysis_section += f"\n{emoji} <b>Posibilidad de contratación: {probability}</b>\n"
        
        message = f"""
🔵 <b>{title}</b>

🏢 <b>Empresa:</b> {company}
📍 <b>Ubicación:</b> {location}
{salary}
🔗 <b>Plataforma:</b> {platform}
{analysis_section}
<b>Aplicar aquí:</b> {apply_link}

{'─' * 40}
"""
        
        return message
        
    except KeyError as e:
        print(f"❌ Error: Campo faltante en datos del trabajo: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado formateando mensaje: {e}")
        return None

{'─' * 40}
"""
    
    return message


def send_to_telegram(job_data: Dict, all_jobs: List[Dict] = None) -> bool:
    """
    Envía la información del trabajo a Telegram
    
    Args:
        job_data: Diccionario con datos del trabajo
        all_jobs: Lista de todos los trabajos (para análisis)
    
    Returns:
        True si se envió correctamente, False en caso contrario
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Token o Chat ID de Telegram no configurados")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        message = format_job_message(job_data, all_jobs)
        
        if not message:
            print("⚠️ No se pudo generar el mensaje")
            return False
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        
        return True
        
    except requests.exceptions.Timeout:
        print(f"⏱️ Timeout enviando mensaje a Telegram")
        return False
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print(f"⚠️ Rate limit de Telegram. Esperando...")
            time.sleep(3)
        else:
            print(f"❌ Error HTTP al enviar a Telegram: {e.response.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Error de conexión con Telegram")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de request a Telegram: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado enviando a Telegram: {e}")
        return False


def main():
    """
    Función principal
    """
    print("=" * 50)
    print("🤖 PulseBot - Buscador de Empleos")
    print("=" * 50)
    
    # Validar configuración
    if not RAPIDAPI_KEY:
        print("❌ ERROR: RAPIDAPI_KEY no configurada")
        print("Por favor, configura tu API key en el archivo .env o GitHub Secrets")
        return
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERROR: Credenciales de Telegram no configuradas")
        print("Por favor, configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en el archivo .env o GitHub Secrets")
        return
    
    print("\n📋 Criterios de búsqueda:")
    print("  - Puesto: Software Engineer")
    print("  - Ubicación: Latin America")
    print("  - Tipo: Remote")
    print("  - Enfoque: Startups")
    print("  - Plataformas: Greenhouse, Lever, BambooHR")
    print()
    
    # Cargar historial de ofertas enviadas
    print("📂 Cargando historial de ofertas enviadas...")
    sent_job_ids = load_sent_jobs()
    print(f"✅ Historial cargado: {len(sent_job_ids)} ofertas previamente enviadas")
    print()
    
    # 1. Buscar trabajos
    jobs = search_jobs(
        query="Software Engineer startup",
        location="Latin America",
        remote_jobs_only=True,
        num_pages=2  # Buscar en 2 páginas para tener más resultados
    )
    
    if not jobs:
        print("❌ No se encontraron trabajos")
        return
    
    # 2. Filtrar por plataforma ATS
    filtered_jobs = filter_jobs_by_platform(jobs)
    
    if not filtered_jobs:
        print("❌ No se encontraron trabajos en las plataformas especificadas")
        return
    
    # 3. Filtrar por startups
    startup_jobs = filter_startup_jobs(filtered_jobs)
    
    # 4. Filtrar trabajos nuevos (no enviados previamente)
    new_jobs = filter_new_jobs(startup_jobs, sent_job_ids)
    
    if not new_jobs:
        print("✅ No hay nuevas ofertas. Todas las ofertas encontradas ya fueron enviadas anteriormente.")
        return
    
    print(f"✨ Encontradas {len(new_jobs)} ofertas nuevas para enviar")
    
    # 5. Limitar a las primeras 5
    jobs_to_send = new_jobs[:5]
    
    print(f"\n📤 Enviando {len(jobs_to_send)} ofertas a Telegram...\n")
    
    # 6. Enviar a Telegram y registrar
    success_count = 0
    newly_sent_ids = set()
    
    for idx, job in enumerate(jobs_to_send, 1):
        print(f"[{idx}/{len(jobs_to_send)}] Enviando: {job.get('job_title', 'N/A')} - {job.get('employer_name', 'N/A')}")
        
        if send_to_telegram(job, jobs):  # Pasar todos los trabajos para contar vacantes
            success_count += 1
            job_id = generate_job_id(job)
            newly_sent_ids.add(job_id)
            print(f"  ✅ Enviado correctamente\n")
        else:
            print(f"  ❌ Error al enviar\n")
        
        # Pausa entre mensajes para evitar rate limiting
        time.sleep(2)
    
    # 7. Actualizar historial
    if newly_sent_ids:
        sent_job_ids.update(newly_sent_ids)
        save_sent_jobs(sent_job_ids)
    
    print(f"\n{'=' * 50}")
    print(f"✨ Proceso completado: {success_count}/{len(jobs_to_send)} ofertas enviadas")
    print(f"📊 Total histórico: {len(sent_job_ids)} ofertas enviadas")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
