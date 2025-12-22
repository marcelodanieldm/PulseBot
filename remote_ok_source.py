"""
RemoteOK Source - API Gratuita (sin límites de requests)
Alternativa a JSearch API para reducir consumo
"""

import requests
import time
from typing import List, Dict, Optional
import hashlib


class RemoteOKSource:
    """
    RemoteOK - API pública y gratuita
    - Sin autenticación requerida
    - Sin límite de requests (respetar rate limiting)
    - Actualización cada 60 segundos
    - Enfoque: trabajos remotos tech
    """
    
    def __init__(self):
        self.base_url = "https://remoteok.com/api"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (PulseBot/3.0)',
            'Accept': 'application/json'
        }
    
    def search_all_jobs(self) -> List[Dict]:
        """
        Obtiene TODOS los trabajos de RemoteOK
        La API devuelve ~200-500 ofertas actualizadas
        """
        try:
            print(f"🔍 Buscando en RemoteOK (API gratuita)...")
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            jobs = response.json()
            
            # Primera entrada es metadata, skip
            if jobs and isinstance(jobs, list):
                jobs = jobs[1:]
            
            print(f"  ✅ {len(jobs)} trabajos obtenidos de RemoteOK")
            return jobs
        
        except requests.exceptions.RequestException as e:
            print(f"  ❌ RemoteOK error: {e}")
            return []
        except Exception as e:
            print(f"  ❌ RemoteOK error inesperado: {e}")
            return []
    
    def filter_by_keywords(self, jobs: List[Dict], keywords: List[str]) -> List[Dict]:
        """
        Filtra trabajos por keywords en position, tags o company
        
        Args:
            jobs: Lista de trabajos de RemoteOK
            keywords: Lista de términos a buscar (ej: ['python', 'backend', 'django'])
        
        Returns:
            Lista de trabajos filtrados
        """
        if not keywords:
            return jobs
        
        filtered = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for job in jobs:
            # Construir texto de búsqueda
            position = job.get('position', '').lower()
            tags = ' '.join(job.get('tags', [])).lower()
            company = job.get('company', '').lower()
            description = job.get('description', '').lower()
            
            search_text = f"{position} {tags} {company} {description}"
            
            # Verificar si alguna keyword está presente
            if any(kw in search_text for kw in keywords_lower):
                filtered.append(job)
        
        return filtered
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """
        Convierte formato RemoteOK al formato estándar de JSearch
        """
        try:
            # RemoteOK puede dar timestamps unix O strings ISO
            date_posted = raw_job.get('date')
            if date_posted:
                try:
                    # Si es string ISO, usar tal cual
                    if isinstance(date_posted, str):
                        # Limpiar formato (RemoteOK usa ++ en lugar de +)
                        date_posted = date_posted.replace('++', '+')
                    else:
                        # Si es timestamp unix, convertir
                        from datetime import datetime
                        date_posted = datetime.utcfromtimestamp(int(date_posted)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
                except Exception:
                    date_posted = None
            
            # Extraer salary si existe
            salary_min = None
            salary_max = None
            if raw_job.get('salary_min'):
                salary_min = raw_job.get('salary_min')
            if raw_job.get('salary_max'):
                salary_max = raw_job.get('salary_max')
            
            # Generar job_id único
            job_id = raw_job.get('id') or self._generate_job_id(raw_job)
            
            # Apply link
            apply_link = raw_job.get('url') or raw_job.get('apply_url', '')
            
            normalized = {
                'job_id': str(job_id),
                'job_title': raw_job.get('position', 'N/A'),
                'employer_name': raw_job.get('company', 'Unknown Company'),
                'employer_logo': raw_job.get('company_logo'),
                'job_description': raw_job.get('description', ''),
                'job_apply_link': apply_link,
                'job_city': None,  # RemoteOK es 100% remote
                'job_country': None,
                'job_is_remote': True,
                'job_posted_at_datetime_utc': date_posted,
                'job_employment_type': 'FULLTIME',
                'job_required_experience': {},
                'job_required_skills': raw_job.get('tags', []),
                'job_salary_currency': 'USD' if salary_min else None,
                'job_salary_period': 'YEAR' if salary_min else None,
                'job_min_salary': salary_min,
                'job_max_salary': salary_max,
                'source': 'RemoteOK'
            }
            
            return normalized
        
        except Exception as e:
            print(f"  ⚠️ Error normalizando job de RemoteOK: {e}")
            return None
    
    def _generate_job_id(self, job: Dict) -> str:
        """Genera ID único si RemoteOK no lo proporciona"""
        unique_string = f"{job.get('position')}|{job.get('company')}|{job.get('date')}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    
    def search_by_role(self, role: str) -> List[Dict]:
        """
        Busca por rol específico
        
        Args:
            role: Rol a buscar (ej: 'python', 'backend', 'devops')
        
        Returns:
            Lista de trabajos normalizados
        """
        all_jobs = self.search_all_jobs()
        
        if not all_jobs:
            return []
        
        # Expandir rol a keywords relacionadas
        keywords = self._expand_role_keywords(role)
        filtered = self.filter_by_keywords(all_jobs, keywords)
        
        # Normalizar a formato estándar
        normalized = []
        for job in filtered:
            normalized_job = self.normalize_job(job)
            if normalized_job:
                normalized.append(normalized_job)
        
        print(f"  📊 {len(normalized)} trabajos filtrados por '{role}'")
        return normalized
    
    def _expand_role_keywords(self, role: str) -> List[str]:
        """
        Expande un rol a keywords relacionadas para mejor matching
        """
        role_lower = role.lower()
        
        # Mapeo de roles a keywords
        keyword_map = {
            'python': ['python', 'django', 'flask', 'fastapi', 'pytorch'],
            'backend': ['backend', 'back-end', 'api', 'server', 'microservices'],
            'frontend': ['frontend', 'front-end', 'react', 'vue', 'angular'],
            'fullstack': ['fullstack', 'full-stack', 'full stack'],
            'devops': ['devops', 'sre', 'infrastructure', 'kubernetes', 'docker'],
            'qa': ['qa', 'quality assurance', 'tester', 'testing', 'automation'],
            'data': ['data engineer', 'data scientist', 'machine learning', 'ml', 'ai'],
            'mobile': ['mobile', 'ios', 'android', 'react native', 'flutter'],
            'blockchain': ['blockchain', 'web3', 'solidity', 'smart contract', 'crypto'],
        }
        
        # Buscar match parcial
        for key, keywords in keyword_map.items():
            if key in role_lower:
                return keywords
        
        # Default: usar el rol tal cual
        return [role_lower]


def test_remote_ok():
    """Función de prueba"""
    source = RemoteOKSource()
    
    print("\n🧪 Test: Buscando trabajos Python en RemoteOK...")
    python_jobs = source.search_by_role('python')
    
    if python_jobs:
        print(f"\n✅ Encontrados {len(python_jobs)} trabajos Python")
        print("\n📋 Primeros 3 trabajos:")
        for i, job in enumerate(python_jobs[:3], 1):
            print(f"\n{i}. {job['job_title']} - {job['employer_name']}")
            print(f"   Tags: {', '.join(job.get('job_required_skills', [])[:5])}")
            print(f"   Link: {job['job_apply_link']}")
            if job.get('job_min_salary'):
                print(f"   Salary: ${job['job_min_salary']:,} - ${job['job_max_salary']:,}")
    else:
        print("❌ No se encontraron trabajos")


if __name__ == "__main__":
    test_remote_ok()
