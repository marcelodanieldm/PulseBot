"""
Demo del sistema de Reputation Check
Muestra cómo funciona el análisis sin necesitar API keys
"""

from job_search import (
    analyze_company_sentiment,
    calculate_hiring_probability,
    count_company_active_jobs
)

def demo_reputation_system():
    """Demostración del sistema de Reputation Check"""
    
    print("\n" + "=" * 70)
    print("🎯 DEMO: Sistema de Reputation Check para PulseBot")
    print("=" * 70)
    
    # Datos de ejemplo simulados
    mock_jobs = [
        {
            'job_title': 'Senior Software Engineer',
            'employer_name': 'TechStartup',
            'job_description': 'Join our amazing team! We are a fast-growing startup with an incredible culture, collaborative environment, and exciting technical challenges. We offer competitive compensation, flexible hours, and great benefits.',
            'job_apply_link': 'https://jobs.lever.co/techstartup/123',
            'job_min_salary': 80000,
            'job_max_salary': 120000,
            'job_salary_currency': 'USD',
            'job_city': 'Remote',
            'job_country': 'Argentina'
        },
        {
            'job_title': 'Backend Developer',
            'employer_name': 'TechStartup',
            'job_description': 'Looking for experienced backend developer',
            'job_apply_link': 'https://jobs.lever.co/techstartup/456'
        },
        {
            'job_title': 'Frontend Developer',
            'employer_name': 'TechStartup',
            'job_description': 'React expert needed',
            'job_apply_link': 'https://jobs.lever.co/techstartup/789'
        },
        {
            'job_title': 'DevOps Engineer',
            'employer_name': 'TechStartup',
            'job_description': 'Cloud infrastructure specialist',
            'job_apply_link': 'https://jobs.lever.co/techstartup/101'
        },
        {
            'job_title': 'Data Scientist',
            'employer_name': 'TechStartup',
            'job_description': 'ML/AI expert',
            'job_apply_link': 'https://jobs.lever.co/techstartup/102'
        },
        {
            'job_title': 'Product Manager',
            'employer_name': 'TechStartup',
            'job_description': 'Lead product strategy',
            'job_apply_link': 'https://jobs.lever.co/techstartup/103'
        },
        {
            'job_title': 'Full Stack Developer',
            'employer_name': 'MegaCorp',
            'job_description': 'Large enterprise looking for developer. Fast-paced environment with tight deadlines and high pressure. Must be available 24/7.',
            'job_apply_link': 'https://jobs.greenhouse.io/megacorp/999'
        }
    ]
    
    # Analizar primera oferta (TechStartup)
    job = mock_jobs[0]
    company = job['employer_name']
    
    print(f"\n📋 Analizando oferta: {job['job_title']} en {company}")
    print("-" * 70)
    
    # 1. Análisis de sentimiento
    print("\n1️⃣ ANÁLISIS DE SENTIMIENTO")
    sentiment = analyze_company_sentiment(company, job['job_description'])
    print(f"   Descripción: \"{job['job_description'][:100]}...\"")
    print(f"   ✅ Resultado: {sentiment}")
    
    # 2. Contador de vacantes
    print("\n2️⃣ CONTADOR DE VACANTES ACTIVAS")
    active_jobs = count_company_active_jobs(company, mock_jobs)
    print(f"   ✅ {company} tiene {active_jobs} vacantes activas")
    print(f"   Puestos encontrados:")
    for j in mock_jobs:
        if j['employer_name'] == company:
            print(f"      - {j['job_title']}")
    
    # 3. Simulación de reviews
    print("\n3️⃣ BÚSQUEDA DE REVIEWS")
    print(f"   Búsqueda: \"{company} employee reviews glassdoor\"")
    has_reviews = True  # Simulado
    mock_review = "Great place to work! Collaborative team, innovative projects, and supportive management. Salary is competitive and benefits are excellent..."
    print(f"   ✅ Review encontrada: \"{mock_review[:100]}...\"")
    
    # 4. Cálculo de probabilidad
    print("\n4️⃣ CÁLCULO DE PROBABILIDAD DE CONTRATACIÓN")
    print(f"   Factores considerados:")
    print(f"      • Vacantes activas: {active_jobs} → {'✅ Alto (+3 pts)' if active_jobs >= 5 else '⚡ Medio (+2 pts)' if active_jobs >= 3 else '💤 Bajo (+1 pt)'}")
    print(f"      • Reviews encontradas: {'Sí' if has_reviews else 'No'} → {'✅ (+1 pt)' if has_reviews else '❌ (0 pts)'}")
    print(f"      • Sentimiento: {sentiment} → {'✅ (+1 pt)' if sentiment == 'Positivo' else '⚡ (0 pts)' if sentiment == 'Neutral' else '❌ (-1 pt)'}")
    
    probability, emoji = calculate_hiring_probability(active_jobs, has_reviews, sentiment)
    print(f"\n   {emoji} RESULTADO: Posibilidad de contratación = {probability}")
    
    # Comparación con otra empresa
    print("\n" + "=" * 70)
    print("📊 COMPARACIÓN: TechStartup vs MegaCorp")
    print("=" * 70)
    
    job2 = mock_jobs[-1]
    company2 = job2['employer_name']
    sentiment2 = analyze_company_sentiment(company2, job2['job_description'])
    active_jobs2 = count_company_active_jobs(company2, mock_jobs)
    has_reviews2 = False  # Simulado
    probability2, emoji2 = calculate_hiring_probability(active_jobs2, has_reviews2, sentiment2)
    
    print(f"\n{'Métrica':<25} {'TechStartup':<20} {'MegaCorp':<20}")
    print("-" * 70)
    print(f"{'Vacantes activas':<25} {active_jobs:<20} {active_jobs2:<20}")
    print(f"{'Sentimiento':<25} {sentiment:<20} {sentiment2:<20}")
    print(f"{'Reviews encontradas':<25} {'Sí':<20} {'No':<20}")
    print(f"{'Probabilidad':<25} {emoji + ' ' + probability:<20} {emoji2 + ' ' + probability2:<20}")
    
    print("\n💡 RECOMENDACIÓN:")
    if probability == "Alta":
        print("   ✅ TechStartup es una excelente oportunidad!")
        print("   📈 Empresa en crecimiento activo con múltiples vacantes")
        print("   🎯 Mayor probabilidad de respuesta y contratación rápida")
    elif probability == "Media":
        print("   ⚡ TechStartup es una oportunidad sólida")
        print("   📊 Actividad de contratación moderada")
    else:
        print("   💤 Evalúa cuidadosamente si esta oportunidad vale la pena")
    
    # Mensaje final formateado
    print("\n" + "=" * 70)
    print("📱 VISTA PREVIA DEL MENSAJE EN TELEGRAM")
    print("=" * 70)
    
    message = f"""
🔵 {job['job_title']}

🏢 Empresa: {company}
📍 Ubicación: {job['job_city']}, {job['job_country']}
💰 ${job['job_min_salary']:,} - ${job['job_max_salary']:,} {job['job_salary_currency']}
🔗 Plataforma: Lever

📊 Análisis de Empresa:
   • Vacantes activas: {active_jobs}
   • Sentimiento: {sentiment}
   • Review: "{mock_review[:120]}..."

{emoji} Posibilidad de contratación: {probability}

Aplicar aquí: {job['job_apply_link']}
────────────────────────────────────────
"""
    
    print(message)
    
    print("=" * 70)
    print("✨ Demo completada - El bot está listo para buscar ofertas reales!")
    print("=" * 70)
    print("\nPróximos pasos:")
    print("1. Configura tus credenciales en el archivo .env")
    print("2. Ejecuta: python job_search.py")
    print("3. Recibe ofertas con análisis completo en tu Telegram\n")

if __name__ == "__main__":
    demo_reputation_system()
