"""
Script de prueba para las funcionalidades de Reputation Check
"""

from job_search import (
    search_company_reviews,
    analyze_company_sentiment,
    calculate_hiring_probability
)

def test_reputation_check():
    """Prueba las funciones de Reputation Check"""
    
    print("=" * 60)
    print("🧪 Prueba de Reputation Check")
    print("=" * 60)
    
    # Test 1: Búsqueda de reviews
    print("\n1️⃣ Buscando reviews de Google...")
    reviews = search_company_reviews("Google")
    if reviews:
        print(f"✅ Reviews encontradas: {reviews[:150]}...")
    else:
        print("❌ No se encontraron reviews")
    
    # Test 2: Análisis de sentimiento
    print("\n2️⃣ Analizando sentimiento...")
    positive_text = "We are an amazing startup with great culture, collaborative team, and exciting challenges!"
    negative_text = "Work long hours, stressful environment, demanding deadlines, no work-life balance"
    neutral_text = "The company provides standard benefits and regular working hours."
    
    sentiment_pos = analyze_company_sentiment("Test Company", positive_text)
    sentiment_neg = analyze_company_sentiment("Test Company", negative_text)
    sentiment_neu = analyze_company_sentiment("Test Company", neutral_text)
    
    print(f"   Texto positivo → {sentiment_pos}")
    print(f"   Texto negativo → {sentiment_neg}")
    print(f"   Texto neutral → {sentiment_neu}")
    
    # Test 3: Cálculo de probabilidad
    print("\n3️⃣ Calculando probabilidad de contratación...")
    
    scenarios = [
        (10, True, "Positivo", "🔥 Alta - Empresa muy activa"),
        (3, True, "Neutral", "⚡ Media - Contratación moderada"),
        (1, False, "Negativo", "💤 Baja - Pocas señales")
    ]
    
    for jobs, has_reviews, sentiment, expected in scenarios:
        prob, emoji = calculate_hiring_probability(jobs, has_reviews, sentiment)
        print(f"   {emoji} {prob} - {jobs} vacantes, reviews: {has_reviews}, sentimiento: {sentiment}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada")
    print("=" * 60)

if __name__ == "__main__":
    test_reputation_check()
