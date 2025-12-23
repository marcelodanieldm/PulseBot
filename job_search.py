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
import sqlite3
from typing import List, Dict, Optional, Tuple, Set
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from textblob import TextBlob
from bs4 import BeautifulSoup

# Importar RemoteOK source
try:
    from remote_ok_source import RemoteOKSource
    REMOTEOK_AVAILABLE = True
except ImportError:
    REMOTEOK_AVAILABLE = False
    print("⚠️ RemoteOK source no disponible")

# Cargar variables de entorno
load_dotenv()

# Configuración
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Plataformas ATS permitidas - Ampliado para IT
ALLOWED_PLATFORMS = [
    # Principales ATS
    'greenhouse.io', 'lever.co', 'bamboohr.com', 'workable.com', 'ashbyhq.com',
    'jobs.lever.co', 'apply.workable.com', 'careers-page',
    
    # ATS corporativos
    'myworkdayjobs.com', 'smartrecruiters.com', 'icims.com', 'successfactors.com',
    'taleo.net', 'ultipro.com', 'paylocity.com', 'jobvite.com',
    
    # ATS de startups y tech
    'recruitee.com', 'breezy.hr', 'greenhouse.com', 'lever.com',
    'workday.com', 'oracle.com', 'sap.com', 'personio.com',
    
    # ATS modernos
    'teamtailor.com', 'pinpointhq.com', 'fountain.com', 'eightfold.ai',
    'jazz.co', 'comeet.com', 'freshteam.com', 'zohorecruit.com',
    
    # Páginas de carrera
    'careers.', 'jobs.', 'apply.', 'recruiting.', 'talent.',
    'opportunities.', 'join.', 'work-with-us', 'we-are-hiring',
    
    # Plataformas específicas de IT y Job Boards
    'stackoverflow.com/jobs', 'angel.co', 'wellfound.com',
    'ycombinator.com', 'remoteok.io', 'weworkremotely.com',
    'remoteok.com', 'remote-jobs', 'jobs/', 'hire/', 'apply/',
    'linkedin.com/jobs', 'indeed.com', 'glassdoor.com'
]

# Base de datos para tracking de ofertas enviadas
DB_FILE = 'processed_jobs.db'

# Diccionarios de clasificación - Ampliado con términos en inglés
CATEGORIES = {
    '🚀 STARTUP': [
        # Etapas de financiamiento
        'series a', 'series b', 'series c', 'seed', 'pre-seed', 'seed stage',
        'early stage', 'growth stage', 'late stage', 'series funding',
        
        # Términos de startup
        'equity', 'stock options', 'esop', 'rsu', 'unicorn', 'decacorn',
        'venture capital', 'vc-backed', 'vc funded', 'venture backed',
        'y combinator', 'techstars', 'accelerator', 'incubator',
        
        # Características
        'fast-growing', 'hyper growth', 'scaling rapidly', 'rapidly growing',
        'high growth', 'exponential growth', 'scaling startup', 'scale up',
        'saas', 'paas', 'iaas', 'product-led', 'product-driven',
        
        # Cultura startup
        'startup culture', 'innovative team', 'disruptive', 'game changer',
        'cutting edge', 'bleeding edge', 'move fast', 'break things',
        'agile startup', 'lean startup', 'mvp focused', 'iteration',
        'startup', 'start-up', 'founded in 20', 'newly funded'
    ],
    '🏢 FACTORY/STAFFING': [
        # Modelos de negocio
        'outsourcing', 'outstaffing', 'staff augmentation', 'body shop',
        'staff leasing', 'talent leasing', 'resource augmentation',
        
        # Servicios
        'client project', 'client projects', 'consultancy', 'consulting firm',
        'professional services', 'managed services', 'it services',
        'digital agency', 'software house', 'development shop',
        
        # Ubicación
        'nearshore', 'offshore', 'onshore', 'distributed team',
        'staff augmentation company', 'it consulting', 'tech consulting',
        
        # Tipo de trabajo
        'b2b services', 'staffing', 'consulting', 'augmentation',
        'client-facing', 'billable hours', 'project-based',
        'contractor', 'contract work', 'contract to hire', 'c2h'
    ],
    '💳 FINTECH/AI': [
        # Fintech
        'fintech', 'financial technology', 'payments', 'payment processing',
        'banking', 'neobank', 'digital bank', 'open banking', 'api banking',
        'wealth management', 'robo advisor', 'investment platform',
        'lending platform', 'peer to peer', 'p2p lending', 'crowdfunding',
        'insurtech', 'regtech', 'wealthtech', 'proptech',
        
        # Crypto/Web3
        'crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'defi',
        'decentralized finance', 'web3', 'web 3.0', 'blockchain',
        'smart contracts', 'dapp', 'nft', 'non-fungible', 'dao',
        'metaverse', 'tokenization', 'stablecoin', 'exchange',
        'solidity', 'solidity developer', 'smart contract developer',
        
        # AI/ML
        'ai', 'artificial intelligence', 'machine learning', 'ml',
        'deep learning', 'neural network', 'llm', 'large language model',
        'generative ai', 'gen ai', 'gpt', 'transformer', 'nlp',
        'natural language processing', 'computer vision', 'cv',
        'reinforcement learning', 'supervised learning', 'data science',
        'predictive analytics', 'ai-powered', 'ml-driven', 'ai platform'
    ],
    '🧪 QA/TESTING': [
        # QA General
        'qa', 'quality assurance', 'quality engineer', 'qa engineer',
        'test engineer', 'testing', 'software testing', 'qa analyst',
        
        # QA Manual
        'manual testing', 'manual qa', 'manual tester', 'functional testing',
        'regression testing', 'smoke testing', 'sanity testing',
        'exploratory testing', 'user acceptance testing', 'uat',
        
        # QA Automation
        'qa automation', 'test automation', 'automation engineer',
        'selenium', 'cypress', 'playwright', 'webdriver', 'appium',
        'junit', 'testng', 'pytest', 'jest', 'mocha',
        
        # SDET
        'sdet', 'software development engineer in test',
        'test development', 'automation framework',
        
        # Performance & Security
        'performance testing', 'load testing', 'stress testing',
        'security testing', 'penetration testing', 'api testing',
        
        # Tools & Methodologies
        'test automation framework', 'ci cd testing', 'agile testing',
        'continuous testing', 'shift left', 'test driven development', 'tdd',
        'behavior driven development', 'bdd', 'cucumber', 'gherkin'
    ]
}

# Keywords de LatAm Match - Ampliado con variaciones en inglés
LATAM_KEYWORDS = [
    # Zona horaria
    'timezone alignment', 'time zone overlap', 'timezone compatible',
    'gmt-3', 'gmt-4', 'gmt-5', 'gmt-6', 'utc-3', 'utc-4', 'utc-5', 'utc-6',
    'est compatible', 'pst overlap', 'us timezone', 'american timezone',
    'timezone friendly', 'working hours overlap', 'overlap with us',
    
    # Idioma
    'spanish', 'spanish speaking', 'spanish speaker', 'bilingual',
    'english and spanish', 'fluent in spanish', 'native spanish',
    'portuguese', 'portuguese speaking', 'spanish/english',
    
    # Región
    'latin america', 'latam', 'latinoamerica', 'south america',
    'central america', 'americas', 'western hemisphere',
    
    # Países específicos
    'argentina', 'argentine', 'buenos aires', 'argentina-based',
    'chile', 'chilean', 'santiago', 'chile-based',
    'colombia', 'colombian', 'bogota', 'medellin', 'colombia-based',
    'mexico', 'mexican', 'mexico city', 'cdmx', 'mexico-based',
    'peru', 'peruvian', 'lima', 'peru-based',
    'brazil', 'brazilian', 'sao paulo', 'rio', 'brazil-based',
    'uruguay', 'uruguayan', 'montevideo', 'uruguay-based',
    'costa rica', 'costa rican', 'san jose', 'costa rica-based',
    'ecuador', 'ecuadorian', 'quito', 'guayaquil',
    'bolivia', 'bolivian', 'la paz',
    'paraguay', 'paraguayan', 'asuncion',
    'venezuela', 'venezuelan', 'caracas',
    
    # Preferencias
    'latam only', 'latam preferred', 'latam candidates', 'latam talent',
    'latin american candidates', 'south american candidates',
    'based in latam', 'located in latam', 'latam residents',
    'must be in latam', 'latam location required', 'latam remote',
    'remote latam', 'remote from latam', 'work from latam',
    
    # Beneficios para LatAm
    'competitive salary for latam', 'usd salary', 'paid in usd',
    'dollar salary', 'international salary', 'global salary'
]

# Configuración de Business Intelligence
GROWTH_THRESHOLD = 3  # Número de vacantes para considerar "High Growth"
GROWTH_DAYS = 7  # Días para análisis de crecimiento
HIGH_RATING_THRESHOLD = 4.0  # Rating mínimo para bonificación


def init_database():
    """
    Inicializa la base de datos SQLite
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_jobs (
                job_id TEXT PRIMARY KEY,
                company_name TEXT,
                job_title TEXT,
                processed_at TEXT,
                category TEXT,
                is_latam_match INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")
    except sqlite3.Error as e:
        print(f"❌ Error inicializando base de datos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado en init_database: {e}")


def is_job_processed(job_id: str) -> bool:
    """
    Verifica si una oferta ya fue procesada
    
    Args:
        job_id: ID único del trabajo
    
    Returns:
        True si ya fue procesada, False si no
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT job_id FROM processed_jobs WHERE job_id = ?', (job_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        print(f"⚠️ Error verificando job_id en DB: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Error inesperado en is_job_processed: {e}")
        return False


def save_processed_job(job_id: str, company: str, title: str, category: str, is_latam: bool):
    """
    Guarda una oferta como procesada
    
    Args:
        job_id: ID único del trabajo
        company: Nombre de la empresa
        title: Título del puesto
        category: Categoría detectada
        is_latam: Si es match de LatAm
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO processed_jobs 
            (job_id, company_name, job_title, processed_at, category, is_latam_match)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            job_id,
            company,
            title,
            time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
            category,
            1 if is_latam else 0
        ))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"⚠️ Error guardando job en DB: {e}")
    except Exception as e:
        print(f"⚠️ Error inesperado en save_processed_job: {e}")


def get_processed_count() -> int:
    """
    Obtiene el total de ofertas procesadas
    
    Returns:
        Número total de ofertas en la DB
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM processed_jobs')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    except sqlite3.Error as e:
        print(f"⚠️ Error obteniendo conteo de DB: {e}")
        return 0
    except Exception as e:
        print(f"⚠️ Error inesperado en get_processed_count: {e}")
        return 0


def get_glassdoor_rating(company_name: str) -> Optional[float]:
    """
    DESHABILITADO: Búsqueda de rating de Glassdoor para evitar rate limits
    Retorna None siempre (el sistema funciona sin ratings)
    
    Args:
        company_name: Nombre de la empresa
    
    Returns:
        None (deshabilitado para evitar rate limits)
    """
    # OPTIMIZACIÓN: Deshabilitado para evitar rate limits de DuckDuckGo
    # El Pulse Score se calcula con otros indicadores disponibles
    return None


def check_growth_indicator(company_name: str) -> Tuple[int, bool]:
    """
    Verifica cuántas vacantes de la empresa hay en los últimos N días
    
    Args:
        company_name: Nombre de la empresa
    
    Returns:
        Tupla (count, is_high_growth) donde:
        - count: Número de vacantes en últimos GROWTH_DAYS días
        - is_high_growth: True si count > GROWTH_THRESHOLD
    """
    if not company_name:
        return 0, False
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Calcular fecha límite (GROWTH_DAYS días atrás)
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=GROWTH_DAYS)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # Contar vacantes de la empresa en el período
        cursor.execute('''
            SELECT COUNT(*) FROM processed_jobs 
            WHERE company_name = ? 
            AND processed_at >= ?
        ''', (company_name, cutoff_str))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        is_high_growth = count > GROWTH_THRESHOLD
        
        if is_high_growth:
            print(f"  🔥 HIGH GROWTH: {count} vacantes en últimos {GROWTH_DAYS} días")
        else:
            print(f"  📊 {count} vacantes en últimos {GROWTH_DAYS} días")
        
        return count, is_high_growth
        
    except sqlite3.Error as e:
        print(f"  ⚠️ Error verificando crecimiento en DB: {e}")
        return 0, False
    except Exception as e:
        print(f"  ⚠️ Error inesperado en check_growth_indicator: {e}")
        return 0, False


def analyze_job_description_sentiment(description: str) -> Tuple[str, float]:
    """
    Analiza el sentimiento de la descripción del trabajo
    
    Args:
        description: Texto de la descripción
    
    Returns:
        Tupla (sentiment_label, polarity_score) donde:
        - sentiment_label: 'Muy Positivo', 'Positivo', 'Neutral', 'Negativo'
        - polarity_score: Valor entre -1.0 y 1.0
    """
    if not description or len(description) < 50:
        return 'Neutral', 0.0
    
    try:
        blob = TextBlob(description)
        polarity = blob.sentiment.polarity
        
        # Clasificación más granular
        if polarity > 0.3:
            sentiment = 'Muy Positivo'
        elif polarity > 0.1:
            sentiment = 'Positivo'
        elif polarity < -0.1:
            sentiment = 'Negativo'
        else:
            sentiment = 'Neutral'
        
        return sentiment, polarity
        
    except Exception as e:
        print(f"  ⚠️ Error analizando sentimiento de descripción: {e}")
        return 'Neutral', 0.0


def calculate_pulse_score(
    category: str,
    glassdoor_rating: Optional[float],
    growth_count: int,
    is_latam: bool,
    sentiment_polarity: float
) -> Tuple[int, str]:
    """
    Calcula el Pulse Score (1-10) basado en múltiples factores
    
    Fórmula:
    - +3 puntos si es STARTUP
    - +2 puntos si Rating > 4.0
    - +3 puntos si tiene > 2 vacantes activas (Growth)
    - +2 puntos si menciona LatAm explícitamente
    - +1 punto si sentimiento es muy positivo (polarity > 0.3)
    - -1 punto si sentimiento es negativo
    
    Args:
        category: Categoría de la empresa
        glassdoor_rating: Rating de Glassdoor (0-5)
        growth_count: Número de vacantes activas
        is_latam: Si menciona LatAm
        sentiment_polarity: Polaridad del sentimiento (-1 a 1)
    
    Returns:
        Tupla (score, tip) donde:
        - score: Puntuación de 1 a 10
        - tip: Consejo personalizado para el usuario
    """
    score = 0
    tips = []
    
    # Factor 1: Es Startup (+3)
    if '🚀 STARTUP' in category:
        score += 3
        tips.append('empresa en etapa de crecimiento')
    
    # Factor 2: Rating alto (+2)
    if glassdoor_rating and glassdoor_rating > HIGH_RATING_THRESHOLD:
        score += 2
        tips.append(f'excelente rating ({glassdoor_rating}/5)')
    
    # Factor 3: Growth (>2 vacantes = +3)
    if growth_count > 2:
        score += 3
        tips.append('está escalando rápido')
    
    # Factor 4: LatAm Match (+2)
    if is_latam:
        score += 2
        tips.append('busca talento LatAm específicamente')
    
    # Factor 5: Sentimiento muy positivo (+1)
    if sentiment_polarity > 0.3:
        score += 1
        tips.append('descripción muy atractiva')
    elif sentiment_polarity < -0.1:
        score -= 1
    
    # Normalizar a escala 1-10
    score = max(1, min(10, score))
    
    # Generar tip personalizado
    if len(tips) > 0:
        tip = f"Esta empresa {', '.join(tips[:2])}"
    else:
        tip = "Revisa bien la descripción y cultura de la empresa"
    
    # Agregar contexto según score
    if score >= 8:
        tip += " - ¡Gran oportunidad! 🎯"
    elif score >= 6:
        tip += " - Vale la pena aplicar"
    elif score >= 4:
        tip += " - Investiga más antes de aplicar"
    else:
        tip += " - Procede con cautela"
    
    return score, tip


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


def classify_job(job: Dict) -> str:
    """
    Clasifica el trabajo según keywords en título y descripción
    
    Args:
        job: Diccionario con datos del trabajo
    
    Returns:
        Categoría detectada (emoji incluido) o '📋 GENERAL' si no match
    """
    try:
        title = (job.get('job_title', '') or '').lower()
        description = (job.get('job_description', '') or '').lower()
        company_desc = (job.get('employer_company_type', '') or '').lower()
        
        # Combinar todo el texto para búsqueda
        full_text = f"{title} {description} {company_desc}"
        
        # Buscar categoría con mayor número de matches
        best_category = '📋 GENERAL'
        max_matches = 0
        
        for category, keywords in CATEGORIES.items():
            matches = sum(1 for keyword in keywords if keyword in full_text)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        # Si encontramos al menos 1 match, usar esa categoría
        if max_matches > 0:
            return best_category
        
        return '📋 GENERAL'
        
    except Exception as e:
        print(f"  ⚠️ Error clasificando trabajo: {e}")
        return '📋 GENERAL'


def is_latam_match(job: Dict) -> bool:
    """
    Verifica si la oferta es un match perfecto para LatAm
    
    Args:
        job: Diccionario con datos del trabajo
    
    Returns:
        True si contiene keywords de LatAm, False si no
    """
    try:
        title = (job.get('job_title', '') or '').lower()
        description = (job.get('job_description', '') or '').lower()
        location = (job.get('job_country', '') or '').lower()
        requirements = (job.get('job_highlights', {}) or {}).get('Qualifications', [])
        requirements_text = ' '.join(requirements).lower() if requirements else ''
        
        # Combinar todo el texto
        full_text = f"{title} {description} {location} {requirements_text}"
        
        # Buscar keywords de LatAm
        for keyword in LATAM_KEYWORDS:
            if keyword in full_text:
                return True
        
        return False
        
    except Exception as e:
        print(f"  ⚠️ Error verificando LatAm match: {e}")
        return False


def detect_niche(job: Dict) -> str:
    """
    Detecta el nicho específico del trabajo (SaaS, Fintech, etc.)
    
    Args:
        job: Diccionario con datos del trabajo
    
    Returns:
        Nicho detectado o 'General'
    """
    try:
        description = (job.get('job_description', '') or '').lower()
        title = (job.get('job_title', '') or '').lower()
        full_text = f"{title} {description}"
        
        # Buscar nichos específicos
        niches = {
            'SaaS': ['saas', 'software as a service', 'cloud platform', 'b2b software'],
            'Fintech': ['fintech', 'payments', 'banking', 'financial technology'],
            'Crypto/Web3': ['crypto', 'blockchain', 'web3', 'defi', 'nft'],
            'AI/ML': ['ai', 'machine learning', 'artificial intelligence', 'llm', 'deep learning'],
            'E-commerce': ['e-commerce', 'ecommerce', 'marketplace', 'retail'],
            'HealthTech': ['healthtech', 'healthcare', 'medical', 'telemedicine'],
            'EdTech': ['edtech', 'education', 'learning platform', 'online courses']
        }
        
        for niche, keywords in niches.items():
            if any(keyword in full_text for keyword in keywords):
                return niche
        
        return 'General'
        
    except Exception as e:
        print(f"  ⚠️ Error detectando nicho: {e}")
        return 'General'


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


def generate_score_bar(score: int, max_score: int = 10) -> str:
    """
    Genera una barra visual para el Pulse Score
    
    Args:
        score: Puntuación actual (1-10)
        max_score: Puntuación máxima (default 10)
    
    Returns:
        Barra visual como string (ej: [⭐⭐⭐⭐-------] 4/10)
    """
    filled = min(score, max_score)
    empty = max_score - filled
    
    bar = '⭐' * filled + '-------'[:empty]
    return f"[{bar}] {score}/{max_score}"


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
        
        # 2. Analizar sentimiento - OPTIMIZADO: Solo análisis local (sin APIs externas)
        sentiment = "Neutral"
        try:
            job_description = job.get('job_description', '')
            # Análisis simple de palabras clave en lugar de APIs externas
            positive_words = ['great', 'excellent', 'amazing', 'innovative', 'growing', 'exciting']
            negative_words = ['urgent', '24/7', 'pressure', 'tight deadline']
            
            desc_lower = job_description.lower()
            positive_count = sum(1 for word in positive_words if word in desc_lower)
            negative_count = sum(1 for word in negative_words if word in desc_lower)
            
            if positive_count > negative_count:
                sentiment = "Positive"
            elif negative_count > positive_count:
                sentiment = "Negative"
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
        
        # === BUSINESS INTELLIGENCE ===
        print(f"  🧠 Calculando Business Intelligence...")
        
        # 5. Glassdoor Rating - DESHABILITADO para evitar rate limits
        glassdoor_rating = None  # Sin búsquedas externas
        
        # 6. Verificar indicador de crecimiento
        growth_count = 0
        is_high_growth = False
        try:
            growth_count, is_high_growth = check_growth_indicator(company)
        except Exception as e:
            print(f"  ⚠️ Error verificando crecimiento: {e}")
        
        # 7. Analizar sentimiento de la descripción del trabajo
        job_sentiment = "Neutral"
        sentiment_polarity = 0.0
        try:
            job_description = job.get('job_description', '')
            job_sentiment, sentiment_polarity = analyze_job_description_sentiment(job_description)
        except Exception as e:
            print(f"  ⚠️ Error analizando sentimiento del job: {e}")
        
        # === CLASIFICACIÓN ===
        # Clasificar el trabajo
        category = classify_job(job)
        
        # Detectar nicho
        niche = detect_niche(job)
        
        # Verificar LatAm match
        latam_fire = ""
        is_latam = is_latam_match(job)
        if is_latam:
            latam_fire = "🔥 "
        
        # 8. Calcular Pulse Score
        pulse_score = 1
        pulse_tip = "Revisa bien la descripción"
        try:
            pulse_score, pulse_tip = calculate_pulse_score(
                category,
                glassdoor_rating,
                growth_count,
                is_latam,
                sentiment_polarity
            )
            print(f"  ⭐ Pulse Score: {pulse_score}/10")
        except Exception as e:
            print(f"  ⚠️ Error calculando Pulse Score: {e}")
        
        # Generar barra visual del score
        score_bar = generate_score_bar(pulse_score)
        
        # Construir sección de análisis básico
        analysis_section = f"\n📊 <b>Análisis de Empresa:</b>\n"
        analysis_section += f"   • Vacantes activas: {active_jobs}\n"
        
        if glassdoor_rating:
            analysis_section += f"   • Rating Glassdoor: {glassdoor_rating}/5 ⭐\n"
        
        if is_high_growth:
            analysis_section += f"   • 🔥 <b>HIGH GROWTH</b>: {growth_count} vacantes en {GROWTH_DAYS} días\n"
        
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
        
        # === PULSE SCORE SECTION ===
        pulse_section = f"\n⚡ <b>Pulse Score:</b> {score_bar}\n"
        pulse_section += f"💡 <b>Tip:</b> {pulse_tip}\n"
        
        # Generar job_id para display
        job_id = generate_job_id(job)
        short_id = job_id[:12] if job_id else "N/A"
        
        message = f"""
{latam_fire}[{category}] <b>{title}</b>

🏢 <b>Empresa:</b> {company}
💰 <b>Nicho:</b> {niche}
📍 <b>Ubicación:</b> {location}
{salary}
🛠️ <b>ATS:</b> {platform}
{analysis_section}
{pulse_section}
🔗 <b>Aplicar aquí:</b> {apply_link}

<code>ID: {short_id}</code>
{'─' * 40}
"""
        
        return message, category, is_latam
        
    except KeyError as e:
        print(f"❌ Error: Campo faltante en datos del trabajo: {e}")
        return None, "📋 GENERAL", False
    except Exception as e:
        print(f"❌ Error inesperado formateando mensaje: {e}")
        return None, "📋 GENERAL", False


def send_to_telegram(job_data: Dict, all_jobs: List[Dict] = None) -> bool:
    """
    Envía la información del trabajo a Telegram y guarda en DB
    
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
        
        result = format_job_message(job_data, all_jobs)
        
        if not result:
            print("⚠️ No se pudo generar el mensaje")
            return False
        
        # Desempaquetar resultado
        message, category, is_latam = result
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        
        # Guardar en DB después de envío exitoso
        job_id = generate_job_id(job_data)
        company = job_data.get('employer_name', 'N/A')
        title = job_data.get('job_title', 'N/A')
        save_processed_job(job_id, company, title, category, is_latam)
        
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
    print("🤖 PulseBot - Buscador de Empleos Inteligente")
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
    
    # Inicializar base de datos
    print("\n🗄️ Inicializando base de datos...")
    init_database()
    
    processed_count = get_processed_count()
    print(f"📊 Ofertas procesadas anteriormente: {processed_count}")
    
    # Búsquedas múltiples en inglés y español con diferentes roles y ubicaciones
    # PRIORIDAD: Búsquedas worldwide y Latam primero
    search_queries = [
        # 🌍 WORLDWIDE + GLOBAL - MÁXIMA PRIORIDAD
        "Software Engineer remote worldwide",
        "Full Stack Developer remote anywhere",
        "QA Engineer remote global",
        "Backend Engineer remote worldwide",
        "DevOps Engineer remote anywhere",
        "Frontend Developer remote worldwide",
        "Python Developer remote anywhere",
        "React Developer remote worldwide",
        "Solidity Developer remote worldwide",
        "Ruby on Rails Developer remote anywhere",
        "Project Manager remote worldwide",
        "Blockchain Developer remote anywhere",
        "Manual QA Tester remote global",
        "TypeScript Developer remote worldwide",
        "Java Developer remote anywhere",
        "Mobile Developer remote global",
        "Data Scientist remote worldwide",
        
        # 🌎 LATAM / LATIN AMERICA - MÁXIMA PRIORIDAD
        "Software Engineer remote Latam",
        "Full Stack Developer remote Latin America",
        "Backend Engineer remote Latam",
        "QA Engineer remote Latin America",
        "DevOps Engineer remote Latam",
        "Frontend Developer remote Latin America",
        "Python Developer remote Latam",
        "React Developer remote Latin America",
        "Solidity Developer remote Latam",
        "Ruby on Rails Developer remote Latin America",
        "Project Manager remote Latam",
        "Blockchain Developer remote Latin America",
        "Manual QA Tester remote Latam",
        "Node.js Developer remote Latin America",
        "Java Developer remote Latam",
        "TypeScript Developer remote Latin America",
        
        # 🇪🇸 BÚSQUEDAS EN ESPAÑOL - NUEVO
        "Ingeniero de Software remoto",
        "Desarrollador Full Stack remoto",
        "Desarrollador Backend remoto",
        "Desarrollador Frontend remoto",
        "Ingeniero QA remoto",
        "Desarrollador Python remoto",
        "Desarrollador React remoto",
        "Ingeniero DevOps remoto",
        "Desarrollador Node.js remoto",
        "Desarrollador Java remoto",
        "Ingeniero de Datos remoto",
        "Desarrollador Web3 remoto",
        
        # Software Engineers
        "Software Engineer remote startup",
        "Full Stack Developer remote",
        "Backend Engineer remote startup", 
        "Frontend Developer remote",
        "Senior Software Engineer remote",
        "Junior Developer remote",
        "Mid-Level Developer remote",
        
        # Infrastructure & DevOps
        "DevOps Engineer remote",
        "Site Reliability Engineer SRE remote",
        "Data Engineer remote",
        "Machine Learning Engineer remote",
        "Cloud Engineer remote",
        "Kubernetes Engineer remote",
        "Infrastructure Engineer remote",
        "Platform Engineer remote",
        
        # Language-specific
        "Python Developer remote",
        "Node.js Developer remote",
        "React Developer remote",
        "Go Developer remote",
        "Rust Engineer remote",
        "TypeScript Developer remote",
        "Java Developer remote",
        "C# Developer remote",
        "PHP Developer remote",
        "Ruby Developer remote",
        "Elixir Developer remote",
        "Scala Developer remote",
        
        # QA Engineers - EXPANDIDO
        "QA Engineer remote",
        "QA Automation Engineer remote",
        "QA Manual Tester remote",
        "Test Automation Engineer remote",
        "Quality Assurance Engineer remote",
        "SDET Software Development Engineer in Test remote",
        "Performance Test Engineer remote",
        "Security Test Engineer remote",
        
        # Blockchain/Web3 - EXPANDIDO
        "Solidity Developer remote",
        "Blockchain Developer remote",
        "Web3 Engineer remote",
        "Smart Contract Developer remote",
        "Crypto Developer remote",
        "DeFi Developer remote",
        "NFT Developer remote",
        
        # Mobile Development - NUEVO
        "Mobile Developer remote",
        "iOS Developer remote",
        "Android Developer remote",
        "React Native Developer remote",
        "Flutter Developer remote",
        
        # Data & AI/ML - NUEVO
        "Data Scientist remote",
        "ML Engineer remote",
        "AI Engineer remote",
        "Data Analyst remote",
        "Business Intelligence Analyst remote",
        
        # Búsquedas por región - Europa
        "Software Engineer remote Europe",
        "Developer remote European Union",
        "QA Engineer remote Europe",
        "Backend Developer remote Spain",
        "Frontend Developer remote Portugal",
        
        # Búsquedas por región - USA
        "Software Engineer remote United States",
        "Full Stack Developer remote USA",
        "QA Engineer remote United States",
        
        # Búsquedas por región - LatAm específico
        "Software Engineer remote Mexico",
        "Developer remote Chile",
        "QA Engineer remote Colombia",
        "Engineer remote Brazil Brasil",
        "Developer remote Argentina",
        "Software Engineer remote Uruguay",
        "Developer remote Costa Rica",
        "Engineer remote Peru",
        
        # Búsquedas por tecnología - NUEVO
        "Django Developer remote",
        "FastAPI Developer remote",
        "Spring Boot Developer remote",
        "Angular Developer remote",
        "Vue.js Developer remote",
        "GraphQL Developer remote",
        "Docker Engineer remote",
        "AWS Engineer remote",
        "Azure Engineer remote"
    ]
    
    print("\n📋 Estrategia Multi-Source OPTIMIZADA (Costo Cero):")
    print(f"  📊 Total queries configuradas: {len(search_queries)}")
    print(f"  ")
    print(f"  🌐 FUENTE PRINCIPAL: RemoteOK API (100% GRATIS)")
    print(f"     - Sin límites, sin autenticación")
    print(f"     - Obtiene TODAS las ofertas remotas disponibles")
    print(f"     - Filtrado inteligente por keywords (ES + EN)")
    print(f"     - Prioridad: Latam + Worldwide")
    print(f"  ")
    print(f"  💡 JSearch API: DESHABILITADO (para evitar rate limits)")
    print(f"     - Activar solo si necesitas más fuentes")
    print(f"     - Cambiar jsearch_enabled = True en el código")
    print(f"  ")
    print(f"  ✅ Total esperado: ~80-150 ofertas por ejecución")
    print(f"  🏢 Filtro ATS: {len(ALLOWED_PLATFORMS)} plataformas")

    
    # 1. JSearch API - DESHABILITADO por defecto (cambiar jsearch_enabled=True para activar)
    jsearch_enabled = False  # Cambiar a True si tienes cuota disponible
    
    all_jobs = []
    if jsearch_enabled:
        print("\n🔥 Búsquedas en JSearch API...")
        for idx, query in enumerate(search_queries[:5], 1):  # Solo 5 para conservar cuota
            print(f"\n🔍 [{idx}/5] JSearch: '{query}'")
            try:
                jobs = search_jobs(
                    query=query,
                    location="",
                    remote_jobs_only=True,
                    num_pages=1
                )
                if jobs:
                    all_jobs.extend(jobs)
                    print(f"  ✅ {len(jobs)} resultados")
                else:
                    print(f"  ⚠️ Sin resultados")
            except Exception as e:
                print(f"  ❌ Error en búsqueda: {e}")
            time.sleep(2)
    else:
        print("\n💡 JSearch API deshabilitado (usando solo RemoteOK - gratis)")
    
    # 1.5 FUENTE PRINCIPAL: RemoteOK (API GRATUITA, SIN LÍMITES)
    if REMOTEOK_AVAILABLE:
        print(f"\n🌐 Obteniendo ofertas de RemoteOK (API gratuita, sin límites)...")
        try:
            remoteok = RemoteOKSource()
            
            # Obtener TODOS los trabajos de RemoteOK
            print(f"  🔍 Descargando todas las ofertas disponibles...")
            all_remoteok_jobs = remoteok.search_all_jobs()
            
            if all_remoteok_jobs:
                # Filtrar por keywords PRIORITARIAS (LatAm + Tech)
                priority_keywords = [
                    # LATAM PRIORITY
                    'latam', 'latin america', 'argentina', 'chile', 'colombia', 'mexico',
                    'brazil', 'peru', 'uruguay', 'remote', 'worldwide', 'anywhere',
                    # Tech roles (inglés)
                    'python', 'backend', 'fullstack', 'full stack', 'devops', 'qa',
                    'frontend', 'react', 'node', 'typescript', 'java', 'go', 'rust',
                    'engineer', 'developer', 'software', 'web3', 'blockchain', 'solidity',
                    'mobile', 'android', 'ios', 'data', 'ml', 'machine learning',
                    'django', 'fastapi', 'spring', 'kubernetes', 'docker',
                    # Tech roles (español)
                    'desarrollador', 'ingeniero', 'programador', 'remoto'
                ]
                
                filtered_remoteok = remoteok.filter_by_keywords(all_remoteok_jobs, priority_keywords)
                
                # Normalizar formato y agregar
                remoteok_jobs = []
                for job in filtered_remoteok:
                    normalized = remoteok.normalize_job(job)
                    if normalized:
                        remoteok_jobs.append(normalized)
                
                all_jobs.extend(remoteok_jobs)
                print(f"  ✅ RemoteOK aportó {len(remoteok_jobs)} ofertas filtradas (de {len(all_remoteok_jobs)} totales)")
            else:
                print(f"  ⚠️ RemoteOK no devolvió resultados")
            
        except Exception as e:
            print(f"  ⚠️ Error en RemoteOK (continuando sin él): {e}")
    else:
        print(f"\n  ⚠️ RemoteOK no disponible. Instala con: pip install requests")
    
    # Eliminar duplicados por job_id
    seen_ids = set()
    unique_jobs = []
    for job in all_jobs:
        if job['job_id'] not in seen_ids:
            seen_ids.add(job['job_id'])
            unique_jobs.append(job)
    
    print(f"\n📊 Total encontrado: {len(all_jobs)} ofertas ({len(unique_jobs)} únicas)")
    
    if not unique_jobs:
        print("❌ No se encontraron trabajos")
        return
    
    # 2. Filtrar por plataforma ATS
    filtered_jobs = filter_jobs_by_platform(unique_jobs)
    print(f"🏢 Filtradas por ATS: {len(filtered_jobs)} ofertas")
    
    if not filtered_jobs:
        print("⚠️ No se encontraron trabajos en las plataformas ATS especificadas")
        print("💡 Tip: Las ofertas encontradas usan otras plataformas. Considera ampliar ALLOWED_PLATFORMS")
        return
    
    # 3. Filtrar por startups
    startup_jobs = filter_startup_jobs(filtered_jobs)
    
    # 4. Filtrar trabajos nuevos (no procesados previamente)
    # Simplificado: filter_new_jobs usa is_job_processed internamente
    new_jobs = [job for job in startup_jobs if not is_job_processed(job['job_id'])]
    
    if not new_jobs:
        print("✅ No hay nuevas ofertas. Todas las ofertas encontradas ya fueron procesadas anteriormente.")
        return
    
    print(f"✨ Encontradas {len(new_jobs)} ofertas nuevas para enviar")
    
    # 5. Limitar a las primeras 20
    jobs_to_send = new_jobs[:20]
    
    print(f"\n📤 Enviando {len(jobs_to_send)} ofertas a Telegram...\n")
    
    # 6. Enviar a Telegram (la DB se actualiza automáticamente en send_to_telegram)
    success_count = 0
    
    for idx, job in enumerate(jobs_to_send, 1):
        print(f"[{idx}/{len(jobs_to_send)}] Enviando: {job.get('job_title', 'N/A')} - {job.get('employer_name', 'N/A')}")
        
        if send_to_telegram(job, startup_jobs):  # Pasar startup_jobs para contar vacantes
            success_count += 1
            print(f"  ✅ Enviado y guardado en DB\n")
        else:
            print(f"  ❌ Error al enviar\n")
        
        # Pausa entre mensajes para evitar rate limiting
        time.sleep(2)
    
    # 7. Mostrar estadísticas finales
    final_count = get_processed_count()
    
    print(f"\n{'=' * 50}")
    print(f"✨ Proceso completado: {success_count}/{len(jobs_to_send)} ofertas enviadas")
    print(f"📊 Total en base de datos: {final_count} ofertas procesadas")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
