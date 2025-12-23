"""
Demo Simple - Solo RemoteOK
Prueba el flujo completo usando únicamente RemoteOK (sin límites)
"""

import time
from remote_ok_source import RemoteOKSource
from job_search import (
    filter_jobs_by_platform,
    filter_startup_jobs,
    is_job_processed,
    send_to_telegram,
    init_database,
    get_processed_count,
    ALLOWED_PLATFORMS
)


def main():
    """Ejecuta búsqueda usando solo RemoteOK"""
    
    print("\n" + "="*70)
    print("🚀 DEMO - Búsqueda Solo con RemoteOK (Sin límites)")
    print("="*70)
    
    # Inicializar base de datos
    print("\n🗄️ Inicializando base de datos...")
    init_database()
    
    processed_count = get_processed_count()
    print(f"📊 Ofertas procesadas anteriormente: {processed_count}")
    
    # 1. Obtener trabajos de RemoteOK
    print("\n🌐 Obteniendo ofertas de RemoteOK...")
    try:
        remoteok = RemoteOKSource()
        
        # Obtener TODOS los trabajos
        print("  🔍 Descargando todas las ofertas disponibles...")
        all_jobs = remoteok.search_all_jobs()
        
        if not all_jobs:
            print("  ❌ RemoteOK no devolvió resultados")
            return
        
        print(f"  ✅ {len(all_jobs)} ofertas obtenidas")
        
        # Filtrar por keywords relevantes (español + inglés)
        print("\n🔍 Filtrando por keywords relevantes...")
        keywords = [
            # Inglés - Roles
            'python', 'backend', 'fullstack', 'full stack', 'devops', 'qa',
            'frontend', 'react', 'node', 'typescript', 'java', 'go', 'rust',
            'engineer', 'developer', 'software', 'web3', 'blockchain', 'solidity',
            'mobile', 'android', 'ios', 'data', 'ml', 'machine learning',
            'django', 'fastapi', 'spring', 'angular', 'vue',
            # Español
            'desarrollador', 'ingeniero', 'programador', 'remoto'
        ]
        
        filtered_jobs = remoteok.filter_by_keywords(all_jobs, keywords)
        print(f"  ✅ {len(filtered_jobs)} ofertas coinciden con keywords")
        
        # Normalizar formato
        print("\n🔄 Normalizando formato...")
        normalized_jobs = []
        for job in filtered_jobs:
            normalized = remoteok.normalize_job(job)
            if normalized:
                normalized_jobs.append(normalized)
        
        print(f"  ✅ {len(normalized_jobs)} ofertas normalizadas")
        
    except Exception as e:
        print(f"  ❌ Error obteniendo trabajos de RemoteOK: {e}")
        return
    
    # 2. Filtrar por plataforma ATS
    print(f"\n🏢 Filtrando por {len(ALLOWED_PLATFORMS)} plataformas ATS permitidas...")
    ats_filtered = filter_jobs_by_platform(normalized_jobs)
    print(f"  ✅ {len(ats_filtered)} ofertas en plataformas ATS válidas")
    
    if not ats_filtered:
        print("\n⚠️ No se encontraron trabajos en las plataformas ATS especificadas")
        print("💡 Tip: RemoteOK tiene muchas ofertas directas. Considera ampliar ALLOWED_PLATFORMS")
        print("\nMostrando ejemplos de URLs encontradas:")
        for job in normalized_jobs[:5]:
            print(f"  - {job.get('job_apply_link', 'N/A')}")
        return
    
    # 3. Filtrar por startups
    print("\n🚀 Filtrando startups y empresas tech...")
    startup_jobs = filter_startup_jobs(ats_filtered)
    print(f"  ✅ {len(startup_jobs)} ofertas de startups/tech")
    
    # 4. Filtrar trabajos nuevos (no procesados)
    print("\n✨ Filtrando ofertas nuevas...")
    new_jobs = [job for job in startup_jobs if not is_job_processed(job['job_id'])]
    
    if not new_jobs:
        print("✅ No hay nuevas ofertas. Todas ya fueron procesadas anteriormente.")
        print(f"\n💡 Total en base de datos: {get_processed_count()} ofertas")
        return
    
    print(f"  ✅ {len(new_jobs)} ofertas nuevas para enviar")
    
    # 5. Limitar a las primeras 10 para demo
    jobs_to_send = new_jobs[:10]
    
    print(f"\n📤 Enviando {len(jobs_to_send)} ofertas a Telegram...\n")
    
    # 6. Mostrar preview sin enviar (para demo)
    print("PREVIEW DE OFERTAS A ENVIAR:")
    print("="*70)
    
    for idx, job in enumerate(jobs_to_send, 1):
        print(f"\n[{idx}/{len(jobs_to_send)}]")
        print(f"  🏢 Empresa: {job.get('employer_name', 'N/A')}")
        print(f"  💼 Puesto: {job.get('job_title', 'N/A')}")
        print(f"  🔗 Link: {job.get('job_apply_link', 'N/A')}")
        print(f"  🌍 Remoto: {'Sí' if job.get('job_is_remote') else 'No'}")
        
        skills = job.get('job_required_skills', [])
        if skills:
            print(f"  🛠️ Skills: {', '.join(skills[:5])}")
    
    # Preguntar si enviar a Telegram
    print("\n" + "="*70)
    print("¿Deseas enviar estas ofertas a Telegram? (s/n)")
    
    try:
        respuesta = input().strip().lower()
        
        if respuesta == 's' or respuesta == 'si' or respuesta == 'yes' or respuesta == 'y':
            print("\n📤 Enviando a Telegram...")
            success_count = 0
            
            for idx, job in enumerate(jobs_to_send, 1):
                print(f"\n[{idx}/{len(jobs_to_send)}] Enviando: {job.get('job_title')} @ {job.get('employer_name')}")
                
                if send_to_telegram(job, normalized_jobs):
                    success_count += 1
                    print("  ✅ Enviado y guardado en DB")
                else:
                    print("  ❌ Error al enviar")
                
                # Pausa entre mensajes
                time.sleep(2)
            
            # Estadísticas finales
            final_count = get_processed_count()
            
            print(f"\n{'=' * 50}")
            print(f"✨ Proceso completado: {success_count}/{len(jobs_to_send)} ofertas enviadas")
            print(f"📊 Total en base de datos: {final_count} ofertas procesadas")
            print(f"{'=' * 50}")
        else:
            print("\n✅ Demo cancelado. No se enviaron ofertas.")
            
    except KeyboardInterrupt:
        print("\n\n✋ Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Programa interrumpido. Saliendo...")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
