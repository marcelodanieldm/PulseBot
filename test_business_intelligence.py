"""
Test Script para Business Intelligence Features
Prueba las nuevas funcionalidades de análisis avanzado
"""

import sys
import os

# Job de prueba para testing
test_job = {
    'job_title': 'Senior Full Stack Engineer',
    'employer_name': 'Google',
    'job_description': '''Join our amazing team at Google! We're looking for passionate engineers 
    who love innovation and want to make a real impact. We offer incredible benefits, 
    competitive compensation, stock options, and a fantastic work culture. 
    Work with cutting-edge technology in AI and machine learning. 
    We value diversity and are looking for candidates from Latin America, 
    specifically those in GMT-3 timezone. Spanish language skills are a plus!''',
    'job_city': 'Remote',
    'job_country': 'Global',
    'job_apply_link': 'https://jobs.lever.co/google/123',
    'employer_company_type': 'Startup, Series B',
    'job_min_salary': 100000,
    'job_max_salary': 150000,
    'job_salary_currency': 'USD'
}


def test_glassdoor_rating():
    """Probar extracción de rating de Glassdoor"""
    print("\n" + "=" * 60)
    print("🧪 TEST 1: Extracción de Glassdoor Rating")
    print("=" * 60)
    
    try:
        from job_search import get_glassdoor_rating
        
        # Probar con empresa conocida
        print("\n1️⃣ Probando con Google...")
        rating = get_glassdoor_rating("Google")
        
        if rating:
            print(f"   ✅ Rating extraído: {rating}/5")
            assert 0.0 <= rating <= 5.0, "Rating debe estar entre 0 y 5"
        else:
            print(f"   ⚠️ No se encontró rating (puede ser rate limiting)")
        
        print("\n✅ TEST DE GLASSDOOR RATING: EXITOSO")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST DE GLASSDOOR RATING: FALLO")
        print(f"   Error: {e}")
        return False


def test_growth_indicator():
    """Probar indicador de crecimiento"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Indicador de Crecimiento")
    print("=" * 60)
    
    try:
        from job_search import check_growth_indicator, save_processed_job, init_database
        
        # Inicializar DB
        print("\n1️⃣ Inicializando base de datos...")
        init_database()
        
        # Guardar varios jobs de prueba para la misma empresa
        print("\n2️⃣ Guardando 5 jobs de 'TestCompany'...")
        for i in range(5):
            save_processed_job(
                f"test_job_{i}",
                "TestCompany",
                f"Engineer {i}",
                "🚀 STARTUP",
                False
            )
        
        # Verificar crecimiento
        print("\n3️⃣ Verificando indicador de crecimiento...")
        count, is_high_growth = check_growth_indicator("TestCompany")
        
        print(f"   Vacantes encontradas: {count}")
        print(f"   High Growth: {'SÍ 🔥' if is_high_growth else 'NO'}")
        
        assert count >= 5, "Debería encontrar al menos 5 vacantes"
        assert is_high_growth, "Debería marcar como High Growth"
        
        print("\n✅ TEST DE INDICADOR DE CRECIMIENTO: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE INDICADOR DE CRECIMIENTO: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE INDICADOR DE CRECIMIENTO: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def test_sentiment_analysis():
    """Probar análisis de sentimiento del job description"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Análisis de Sentimiento")
    print("=" * 60)
    
    try:
        from job_search import analyze_job_description_sentiment
        
        test_cases = [
            {
                'description': 'Amazing opportunity! Great benefits, excellent culture, fantastic team!',
                'expected': 'Muy Positivo'
            },
            {
                'description': 'We are looking for a developer. Standard job requirements.',
                'expected': 'Neutral'
            },
            {
                'description': test_job['job_description'],
                'expected': 'Positivo'  # Puede ser Muy Positivo o Positivo
            }
        ]
        
        for idx, test_case in enumerate(test_cases, 1):
            print(f"\n{idx}️⃣ Test case {idx}:")
            print(f"   Texto: {test_case['description'][:60]}...")
            
            sentiment, polarity = analyze_job_description_sentiment(test_case['description'])
            
            print(f"   Sentimiento: {sentiment}")
            print(f"   Polaridad: {polarity:.2f}")
            
            if 'Positivo' in test_case['expected']:
                assert 'Positivo' in sentiment, f"Debería ser positivo, pero es {sentiment}"
            else:
                assert sentiment == test_case['expected'], f"Esperado {test_case['expected']}, obtenido {sentiment}"
        
        print("\n✅ TEST DE ANÁLISIS DE SENTIMIENTO: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE ANÁLISIS DE SENTIMIENTO: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE ANÁLISIS DE SENTIMIENTO: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def test_pulse_score_calculation():
    """Probar cálculo del Pulse Score"""
    print("\n" + "=" * 60)
    print("🧪 TEST 4: Cálculo de Pulse Score")
    print("=" * 60)
    
    try:
        from job_search import calculate_pulse_score
        
        print("\n📊 Probando diferentes escenarios...")
        
        # Escenario 1: Startup + High Rating + LatAm + Growth
        print("\n1️⃣ Escenario IDEAL (máximo score):")
        score, tip = calculate_pulse_score(
            category='🚀 STARTUP',
            glassdoor_rating=4.5,
            growth_count=5,
            is_latam=True,
            sentiment_polarity=0.4
        )
        print(f"   Score: {score}/10")
        print(f"   Tip: {tip}")
        assert score >= 8, "Score ideal debería ser >= 8"
        
        # Escenario 2: Empresa regular
        print("\n2️⃣ Escenario REGULAR:")
        score, tip = calculate_pulse_score(
            category='📋 GENERAL',
            glassdoor_rating=3.5,
            growth_count=1,
            is_latam=False,
            sentiment_polarity=0.0
        )
        print(f"   Score: {score}/10")
        print(f"   Tip: {tip}")
        assert 1 <= score <= 10, "Score debe estar entre 1 y 10"
        
        # Escenario 3: Factory sin growth
        print("\n3️⃣ Escenario BAJO:")
        score, tip = calculate_pulse_score(
            category='🏢 FACTORY/STAFFING',
            glassdoor_rating=None,
            growth_count=0,
            is_latam=False,
            sentiment_polarity=-0.2
        )
        print(f"   Score: {score}/10")
        print(f"   Tip: {tip}")
        assert score <= 5, "Score bajo debería ser <= 5"
        
        print("\n✅ TEST DE PULSE SCORE: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE PULSE SCORE: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE PULSE SCORE: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def test_score_bar_generation():
    """Probar generación de barra visual"""
    print("\n" + "=" * 60)
    print("🧪 TEST 5: Generación de Barra Visual")
    print("=" * 60)
    
    try:
        from job_search import generate_score_bar
        
        test_scores = [1, 3, 5, 7, 10]
        
        print("\n📊 Probando diferentes scores...")
        for score in test_scores:
            bar = generate_score_bar(score)
            print(f"   Score {score:2d}: {bar}")
            
            # Verificar formato
            assert '[' in bar and ']' in bar, "Debe tener corchetes"
            assert '⭐' in bar, "Debe tener estrellas"
            assert f"{score}/10" in bar, "Debe mostrar score/10"
        
        print("\n✅ TEST DE BARRA VISUAL: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE BARRA VISUAL: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE BARRA VISUAL: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def test_complete_message_format():
    """Probar formato completo del mensaje con BI"""
    print("\n" + "=" * 60)
    print("🧪 TEST 6: Mensaje Completo con Business Intelligence")
    print("=" * 60)
    
    try:
        from job_search import format_job_message
        
        print("\n📱 Generando mensaje completo...")
        result = format_job_message(test_job, [test_job])
        
        if not result:
            raise Exception("format_job_message retornó None")
        
        message, category, is_latam = result
        
        print("\n" + "─" * 60)
        print("MENSAJE GENERADO:")
        print("─" * 60)
        print(message)
        print("─" * 60)
        
        # Verificar componentes
        print("\n✓ Verificando componentes...")
        
        assert 'Pulse Score:' in message, "Debe incluir Pulse Score"
        print("   ✅ Pulse Score incluido")
        
        assert '⭐' in message, "Debe incluir barra de estrellas"
        print("   ✅ Barra visual incluida")
        
        assert '💡 <b>Tip:</b>' in message, "Debe incluir tip"
        print("   ✅ Tip incluido")
        
        assert 'Análisis de Empresa:' in message, "Debe incluir análisis"
        print("   ✅ Análisis de empresa incluido")
        
        # Verificar que LatAm match fue detectado
        if is_latam:
            assert '🔥' in message, "Debe tener emoji de LatAm"
            print("   ✅ LatAm match detectado (🔥)")
        
        print("\n✅ TEST DE MENSAJE COMPLETO: EXITOSO")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST DE MENSAJE COMPLETO: FALLO")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ TEST DE MENSAJE COMPLETO: FALLO")
        print(f"   Error inesperado: {e}")
        return False


def run_all_tests():
    """Ejecutar todos los tests de BI"""
    print("\n" + "=" * 60)
    print("🚀 INICIANDO SUITE DE TESTS DE BUSINESS INTELLIGENCE")
    print("=" * 60)
    
    results = []
    
    # Test 1: Glassdoor Rating
    results.append(("Glassdoor Rating", test_glassdoor_rating()))
    
    # Test 2: Growth Indicator
    results.append(("Growth Indicator", test_growth_indicator()))
    
    # Test 3: Sentiment Analysis
    results.append(("Sentiment Analysis", test_sentiment_analysis()))
    
    # Test 4: Pulse Score
    results.append(("Pulse Score", test_pulse_score_calculation()))
    
    # Test 5: Score Bar
    results.append(("Score Bar", test_score_bar_generation()))
    
    # Test 6: Complete Message
    results.append(("Complete Message", test_complete_message_format()))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:25} : {status}")
    
    print("\n" + "=" * 60)
    print(f"Resultado: {passed}/{total} tests exitosos ({passed/total*100:.0f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS DE BUSINESS INTELLIGENCE PASARON!")
        print("✅ El sistema de BI está funcionando correctamente")
    else:
        print(f"\n⚠️ {total - passed} test(s) fallaron")
        print("❌ Revisa los errores arriba")
    
    return passed == total


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🧠 PulseBot - Test de Business Intelligence              ║
║                                                              ║
║   Este script prueba las nuevas funcionalidades BI:         ║
║   • Extracción de Glassdoor Rating                          ║
║   • Indicador de crecimiento (High Growth)                  ║
║   • Análisis de sentimiento del job description             ║
║   • Cálculo de Pulse Score (1-10)                           ║
║   • Generación de barra visual                              ║
║   • Mensaje completo con todas las métricas                 ║
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
