#!/usr/bin/env python3
"""
Test Script - Verificar Configuración de PulseBot para GitHub Actions
"""

import os
import sys
from pathlib import Path

def check_env_variables():
    """Verificar que las variables de entorno estén configuradas"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = {
        'RAPIDAPI_KEY': 'RapidAPI Key (JSearch)',
        'TELEGRAM_BOT_TOKEN': 'Token del Bot de Telegram',
        'TELEGRAM_CHAT_ID': 'ID del Chat/Canal de Telegram'
    }
    
    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
            print(f"  ✅ {var}: {masked}")
        else:
            print(f"  ❌ {var}: NO ENCONTRADO")
            missing.append((var, description))
    
    if missing:
        print("\n⚠️  Variables faltantes:")
        for var, desc in missing:
            print(f"  • {var}: {desc}")
        print("\n💡 Solución:")
        print("  1. Crea un archivo .env en la raíz del proyecto")
        print("  2. Agrega las variables:")
        for var, _ in missing:
            print(f"     {var}=tu_valor_aqui")
        return False
    
    print("✅ Todas las variables de entorno están configuradas\n")
    return True

def check_database():
    """Verificar que la base de datos existe"""
    print("🔍 Verificando base de datos...")
    
    db_file = Path('processed_jobs.db')
    if db_file.exists():
        size = db_file.stat().st_size
        print(f"  ✅ processed_jobs.db existe ({size} bytes)")
        return True
    else:
        print("  ⚠️  processed_jobs.db no existe")
        print("  💡 Se creará automáticamente en la primera ejecución")
        return True

def check_requirements():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_modules = {
        'requests': 'requests',
        'dotenv': 'python-dotenv',
        'duckduckgo_search': 'duckduckgo-search',
        'textblob': 'textblob',
        'bs4': 'beautifulsoup4'
    }
    
    missing = []
    for module, package in required_modules.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Dependencias faltantes:")
        print("  pip install " + " ".join(missing))
        return False
    
    print("✅ Todas las dependencias están instaladas\n")
    return True

def check_workflow():
    """Verificar que el workflow de GitHub Actions existe"""
    print("🔍 Verificando workflow de GitHub Actions...")
    
    workflow_file = Path('.github/workflows/pulsebot_run.yml')
    if workflow_file.exists():
        print(f"  ✅ {workflow_file}")
        
        # Leer y verificar configuración
        content = workflow_file.read_text(encoding='utf-8')
        
        checks = [
            ('cron', 'Ejecución automática cada 4 horas'),
            ('workflow_dispatch', 'Ejecución manual habilitada'),
            ('secrets.RAPIDAPI_KEY', 'Secret RAPIDAPI_KEY configurado'),
            ('secrets.TELEGRAM_BOT_TOKEN', 'Secret TELEGRAM_BOT_TOKEN'),
            ('secrets.TELEGRAM_CHAT_ID', 'Secret TELEGRAM_CHAT_ID'),
            ('processed_jobs.db', 'Persistencia de base de datos')
        ]
        
        for keyword, description in checks:
            if keyword in content:
                print(f"    ✅ {description}")
            else:
                print(f"    ❌ {description}")
        
        return True
    else:
        print(f"  ❌ {workflow_file} no existe")
        return False

def check_gitignore():
    """Verificar que .gitignore está configurado correctamente"""
    print("\n🔍 Verificando .gitignore...")
    
    gitignore = Path('.gitignore')
    if gitignore.exists():
        content = gitignore.read_text(encoding='utf-8')
        
        # Verificar que .env está ignorado
        if '.env' in content and 'processed_jobs.db' not in content:
            print("  ✅ .env está ignorado (seguridad)")
            print("  ✅ processed_jobs.db NO está ignorado (persistencia)")
            return True
        else:
            print("  ⚠️  Configuración de .gitignore incorrecta")
            return False
    else:
        print("  ⚠️  .gitignore no existe")
        return False

def print_next_steps():
    """Imprimir los siguientes pasos"""
    print("\n" + "="*70)
    print("📋 SIGUIENTES PASOS")
    print("="*70)
    
    print("\n1️⃣  Commitear y pushear los archivos:")
    print("    git add .github/workflows/pulsebot_run.yml")
    print("    git add GITHUB_SECRETS_GUIDE.md")
    print("    git add processed_jobs.db")
    print("    git commit -m '🤖 Add GitHub Actions workflow for automation'")
    print("    git push origin main")
    
    print("\n2️⃣  Configurar GitHub Secrets:")
    print("    • Ve a: Settings → Secrets and variables → Actions")
    print("    • Agrega los 3 secrets:")
    print("      - RAPIDAPI_KEY")
    print("      - TELEGRAM_BOT_TOKEN")
    print("      - TELEGRAM_CHAT_ID")
    print("    📖 Guía completa: GITHUB_SECRETS_GUIDE.md")
    
    print("\n3️⃣  Configurar permisos de GitHub Actions:")
    print("    • Ve a: Settings → Actions → General")
    print("    • En 'Workflow permissions', selecciona:")
    print("      ✅ Read and write permissions")
    
    print("\n4️⃣  Probar el workflow:")
    print("    • Ve a: Actions → PulseBot Automated Job Search")
    print("    • Haz clic en 'Run workflow'")
    print("    • Monitorea los logs para verificar que funciona")
    
    print("\n5️⃣  Verificar en Telegram:")
    print("    • Deberías recibir ofertas de empleo en tu canal")
    print("    • Verifica que incluyen Business Intelligence (Pulse Score)")
    
    print("\n🎉 ¡Tu bot se ejecutará automáticamente cada 4 horas!")
    print("="*70 + "\n")

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🤖 PULSEBOT - VERIFICACIÓN DE CONFIGURACIÓN PARA GITHUB ACTIONS")
    print("="*70 + "\n")
    
    checks = [
        check_env_variables(),
        check_requirements(),
        check_database(),
        check_workflow(),
        check_gitignore()
    ]
    
    print("\n" + "="*70)
    if all(checks):
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("="*70)
        print_next_steps()
        return 0
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("="*70)
        print("\n💡 Revisa los errores arriba y corrígelos antes de continuar\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
