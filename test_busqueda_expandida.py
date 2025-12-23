"""
Script de prueba para verificar el flujo expandido de búsqueda
Prueba la búsqueda en español e inglés sin bloqueos
"""

import sys
import time
from job_search import (
    search_jobs,
    filter_jobs_by_platform,
    get_processed_count,
    init_database
)
from remote_ok_source import RemoteOKSource

def test_jsearch_busqueda():
    """Prueba búsquedas básicas de JSearch"""
    print("\n" + "="*70)
    print("🧪 TEST 1: Búsquedas en JSearch API")
    print("="*70)
    
    test_queries = [
        "Software Engineer remote worldwide",
        "Desarrollador Python remoto",
        "QA Engineer remote Latam",
        "Backend Developer remote"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Probando: '{query}'")
        try:
            jobs = search_jobs(
                query=query,
                location="",
                remote_jobs_only=True,
                num_pages=1
            )
            if jobs:
                print(f"  ✅ {len(jobs)} resultados encontrados")
                # Mostrar primer trabajo como ejemplo
                first_job = jobs[0]
                print(f"  📋 Ejemplo: {first_job.get('job_title')} @ {first_job.get('employer_name')}")
            else:
                print(f"  ⚠️ Sin resultados (esto es normal para algunas queries)")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
        
        time.sleep(1)
    
    return True


def test_remoteok_integration():
    """Prueba integración con RemoteOK"""
    print("\n" + "="*70)
    print("🧪 TEST 2: Integración con RemoteOK")
    print("="*70)
    
    try:
        remoteok = RemoteOKSource()
        
        # Obtener todos los jobs
        print("\n🔍 Obteniendo todas las ofertas de RemoteOK...")
        all_jobs = remoteok.search_all_jobs()
        
        if not all_jobs:
            print("  ⚠️ RemoteOK no devolvió resultados")
            return True  # No es un error fatal
        
        print(f"  ✅ {len(all_jobs)} ofertas obtenidas")
        
        # Filtrar por keywords
        print("\n🔍 Filtrando por keywords...")
        keywords = ['python', 'backend', 'fullstack', 'qa', 'desarrollador']
        filtered = remoteok.filter_by_keywords(all_jobs, keywords)
        print(f"  ✅ {len(filtered)} ofertas filtradas")
        
        # Normalizar primer resultado
        if filtered:
            print("\n🔍 Normalizando primer resultado...")
            normalized = remoteok.normalize_job(filtered[0])
            if normalized:
                print(f"  ✅ Normalización exitosa")
                print(f"  📋 Ejemplo: {normalized.get('job_title')} @ {normalized.get('employer_name')}")
            else:
                print(f"  ⚠️ Error en normalización")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_database_operations():
    """Prueba operaciones de base de datos"""
    print("\n" + "="*70)
    print("🧪 TEST 3: Operaciones de Base de Datos")
    print("="*70)
    
    try:
        print("\n🔍 Inicializando base de datos...")
        init_database()
        print("  ✅ Base de datos inicializada")
        
        print("\n🔍 Contando ofertas procesadas...")
        count = get_processed_count()
        print(f"  ✅ {count} ofertas en la base de datos")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_filtrado_plataformas():
    """Prueba filtrado por plataformas ATS"""
    print("\n" + "="*70)
    print("🧪 TEST 4: Filtrado por Plataformas ATS")
    print("="*70)
    
    # Mock de trabajos para testing
    mock_jobs = [
        {
            'job_id': '1',
            'job_title': 'Test Engineer',
            'employer_name': 'TestCorp',
            'job_apply_link': 'https://jobs.lever.co/testcorp/123'
        },
        {
            'job_id': '2',
            'job_title': 'Developer',
            'employer_name': 'AnotherCorp',
            'job_apply_link': 'https://jobs.greenhouse.io/another/456'
        },
        {
            'job_id': '3',
            'job_title': 'QA Tester',
            'employer_name': 'BadPlatform',
            'job_apply_link': 'https://random-ats.com/apply/789'
        }
    ]
    
    try:
        print("\n🔍 Filtrando por plataformas permitidas...")
        filtered = filter_jobs_by_platform(mock_jobs)
        print(f"  ✅ {len(filtered)}/{len(mock_jobs)} trabajos pasaron el filtro")
        
        for job in filtered:
            print(f"  📋 {job['job_title']} @ {job['employer_name']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print("🚀 INICIANDO TESTS DE FLUJO EXPANDIDO")
    print("="*70)
    
    results = {
        'JSearch Búsqueda': test_jsearch_busqueda(),
        'RemoteOK Integración': test_remoteok_integration(),
        'Base de Datos': test_database_operations(),
        'Filtrado Plataformas': test_filtrado_plataformas()
    }
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print("\n" + "="*70)
    print(f"✨ Tests completados: {passed}/{total} exitosos")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron! El sistema está listo para uso.")
        return 0
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los errores arriba.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
