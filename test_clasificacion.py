"""
Test Script para Verificar las Mejoras de Clasificación
Prueba las nuevas funciones sin hacer llamadas a APIs externas
"""

import sys
import os

# Simular datos de ejemplo para testing
test_jobs = [
    {
        'job_title': 'Senior Python Engineer',
        'employer_name': 'StartupXYZ',
        'job_description': '''We are a Series A SaaS startup looking for talented engineers. 
        We offer equity and stock options. Fast-growing company with venture capital backing.
        Looking for candidates in GMT-3 timezone. Spanish fluency required.''',
        'job_city': 'Remote',
        'job_country': 'Argentina',
        'job_apply_link': 'https://jobs.lever.co/startupxyz/123',
        'employer_company_type': 'Startup'
    },
    {
        'job_title': 'Java Developer',
        'employer_name': 'TechConsulting Inc',
        'job_description': '''Join our nearshore team working on client projects. 
        Staff augmentation model. We provide consulting services for multiple B2B clients.
        Offshore development opportunities.''',
        'job_city': 'Multiple',
        'job_country': 'Remote',
        'job_apply_link': 'https://jobs.greenhouse.io/techconsulting/456'
    },
    {
        'job_title': 'ML Engineer',
        'employer_name': 'CryptoBank',
        'job_description': '''Build AI-powered fintech solutions using LLMs and machine learning.
        Experience with blockchain, crypto payments, and Web3 technologies required.
        Deep learning and neural networks experience preferred.''',
        'job_city': 'San Francisco',
        'job_country': 'USA',
        'job_apply_link': 'https://jobs.lever.co/cryptobank/789',
        'employer_company_type': 'Fintech'
    },
    {
        'job_title': 'Frontend Developer',
        'employer_name': 'GenericCorp',
        'job_description': '''Looking for a frontend developer to work on our website.
        Standard corporate role with good benefits.''',
        'job_city': 'New York',
        'job_country': 'USA',
        'job_apply_link': 'https://genericcorp.com/careers/abc'
    }
]

def test_database():
    """Probar funciones de base de datos"""
    print("\n" + "=" * 60)
    print("🧪 TEST 1: Base de Datos SQLite")
    print("=" * 60)
    
    try:
        from job_search import init_database, get_processed_count, save_processed_job, is_job_processed
        
        # Inicializar DB
        print("\n1️⃣ Inicializando base de datos...")
        init_database()
        
        # Obtener conteo
        count = get_processed_count()
        print(f"   ✅ Ofertas en DB: {count}")
        
        # Guardar job de prueba
        print("\n2️⃣ Guardando job de prueba...")
        test_id = "test_job_123"
        save_processed_job(test_id, "TestCompany", "Test Engineer", "🚀 STARTUP", True)
        print("   ✅ Job guardado")
        
        # Verificar si existe
        print("\n3️⃣ Verificando existencia...")
        exists = is_job_processed(test_id)
        print(f"   ✅ Job existe en DB: {exists}")
        
        # Nuevo conteo
        new_count = get_processed_count()
        print(f"\n4️⃣ Nuevo total: {new_count} ofertas")
        
        print("\n✅ TEST DE BASE DE DATOS: EXITOSO")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST DE BASE DE DATOS: FALLO")
        print(f"   Error: {e}")
        return False


def test_classification():
    """Probar funciones de clasificación"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Sistema de Clasificación")
    print("=" * 60)
    
    try:
        from job_search import classify_job, is_latam_match, detect_niche
        
        results = []
        
        for idx, job in enumerate(test_jobs, 1):
            print(f"\n📋 Job {idx}: {job['job_title']} - {job['employer_name']}")
            print("-" * 60)
            
            # Clasificar
            category = classify_job(job)
            print(f"   Categoría: {category}")
            
            # LatAm match
            latam = is_latam_match(job)
            print(f"   LatAm Match: {'🔥 SÍ' if latam else '❌ NO'}")
            
            # Nicho
            niche = detect_niche(job)
            print(f"   Nicho: {niche}")
            
            results.append({
                'job': job['job_title'],
                'category': category,
                'latam': latam,
                'niche': niche
            })
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE CLASIFICACIÓN")
        print("=" * 60)
        
        # Job 1: Debería ser STARTUP + LatAm Match
        assert results[0]['category'] == '🚀 STARTUP', "Job 1 debería ser STARTUP"
        assert results[0]['latam'] == True, "Job 1 debería ser LatAm match"
        print("✅ Job 1: STARTUP + LatAm ✓")
        
        # Job 2: Debería ser FACTORY/STAFFING
        assert results[1]['category'] == '🏢 FACTORY/STAFFING', "Job 2 debería ser FACTORY/STAFFING"
        print("✅ Job 2: FACTORY/STAFFING ✓")
        
        # Job 3: Debería ser FINTECH/AI
        assert results[2]['category'] == '💳 FINTECH/AI', "Job 3 debería ser FINTECH/AI"
        assert results[2]['niche'] in ['Crypto/Web3', 'AI/ML', 'Fintech'], "Job 3 debería tener nicho detectado"
        print("✅ Job 3: FINTECH/AI + Nicho ✓")
        
        # Job 4: Debería ser GENERAL
        assert results[3]['category'] == '📋 GENERAL', "Job 4 debería ser GENERAL"
        print("✅ Job 4: GENERAL ✓")
        
        print("\n✅ TEST DE CLASIFICACIÓN: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE CLASIFICACIÓN: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE CLASIFICACIÓN: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def test_job_id_generation():
    """Probar generación de IDs únicos"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Generación de Job IDs")
    print("=" * 60)
    
    try:
        from job_search import generate_job_id
        
        # Generar IDs para los mismos jobs
        print("\n1️⃣ Generando IDs para jobs de prueba...")
        ids = []
        for job in test_jobs:
            job_id = generate_job_id(job)
            ids.append(job_id)
            print(f"   {job['job_title'][:30]:30} → {job_id[:12]}...")
        
        # Verificar unicidad
        print("\n2️⃣ Verificando unicidad...")
        assert len(ids) == len(set(ids)), "IDs deben ser únicos"
        print("   ✅ Todos los IDs son únicos")
        
        # Verificar consistencia (mismo job → mismo ID)
        print("\n3️⃣ Verificando consistencia...")
        id_again = generate_job_id(test_jobs[0])
        assert ids[0] == id_again, "Mismo job debe generar mismo ID"
        print("   ✅ IDs son consistentes")
        
        # Verificar longitud
        print("\n4️⃣ Verificando formato...")
        for job_id in ids:
            assert isinstance(job_id, str), "ID debe ser string"
            assert len(job_id) > 10, "ID debe tener longitud suficiente"
        print("   ✅ Formato de IDs correcto")
        
        print("\n✅ TEST DE JOB IDs: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE JOB IDs: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE JOB IDs: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def test_message_format():
    """Probar formato de mensaje"""
    print("\n" + "=" * 60)
    print("🧪 TEST 4: Formato de Mensaje en Telegram")
    print("=" * 60)
    
    try:
        from job_search import format_job_message
        
        print("\n📱 Generando mensaje de prueba...")
        result = format_job_message(test_jobs[0], test_jobs)
        
        if not result:
            raise Exception("format_job_message retornó None")
        
        message, category, is_latam = result
        
        print("\n" + "─" * 60)
        print("MENSAJE GENERADO:")
        print("─" * 60)
        print(message)
        print("─" * 60)
        
        # Verificar componentes del mensaje
        print("\n✓ Verificando componentes...")
        
        assert '🔥' in message, "Debería tener emoji de LatAm match"
        print("   ✅ Emoji de LatAm (🔥)")
        
        assert category in message, "Debería tener categoría"
        print(f"   ✅ Categoría ({category})")
        
        assert '🏢 <b>Empresa:</b>' in message, "Debería tener sección de empresa"
        print("   ✅ Sección de empresa")
        
        assert '💰 <b>Nicho:</b>' in message, "Debería tener nicho"
        print("   ✅ Nicho detectado")
        
        assert '🛠️ <b>ATS:</b>' in message, "Debería tener ATS"
        print("   ✅ ATS platform")
        
        assert 'ID:' in message, "Debería tener ID"
        print("   ✅ Job ID")
        
        assert '📊 <b>Análisis de Empresa:</b>' in message, "Debería tener análisis"
        print("   ✅ Análisis de reputación")
        
        print("\n✅ TEST DE FORMATO: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE FORMATO: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE FORMATO: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 60)
    print("🚀 INICIANDO SUITE DE TESTS DE CLASIFICACIÓN")
    print("=" * 60)
    
    results = []
    
    # Test 1: Base de datos
    results.append(("Base de Datos", test_database()))
    
    # Test 2: Clasificación
    results.append(("Clasificación", test_classification()))
    
    # Test 3: Job IDs
    results.append(("Job IDs", test_job_id_generation()))
    
    # Test 4: Formato de mensaje
    results.append(("Formato Mensaje", test_message_format()))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:20} : {status}")
    
    print("\n" + "=" * 60)
    print(f"Resultado: {passed}/{total} tests exitosos ({passed/total*100:.0f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ El sistema de clasificación está funcionando correctamente")
    else:
        print(f"\n⚠️ {total - passed} test(s) fallaron")
        print("❌ Revisa los errores arriba")
    
    return passed == total


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🤖 PulseBot - Test de Sistema de Clasificación           ║
║                                                              ║
║   Este script prueba las nuevas funcionalidades:            ║
║   • Base de datos SQLite                                    ║
║   • Clasificación por categorías                            ║
║   • Detección de LatAm matches                              ║
║   • Detección de nichos                                     ║
║   • Generación de IDs únicos                                ║
║   • Formato de mensajes                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrumpidos por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico ejecutando tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
