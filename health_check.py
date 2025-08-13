#!/usr/bin/env python3
"""
Script de verificación completa del sistema para diagnosticar
todos los componentes necesarios para la conversión de documentos.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_main.settings')
django.setup()

from django.conf import settings

def check_django_config():
    """Verificar configuración de Django."""
    print("🔍 Verificando configuración de Django...")
    
    try:
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"✅ MAX_UPLOAD_SIZE: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB")
        print(f"✅ ALLOWED_UPLOAD_EXTENSIONS: {settings.ALLOWED_UPLOAD_EXTENSIONS}")
        return True
    except Exception as e:
        print(f"❌ Error en configuración Django: {e}")
        return False

def check_directories():
    """Verificar que los directorios necesarios existan."""
    print("\n🔍 Verificando directorios...")
    
    directories = [
        settings.MEDIA_ROOT,
        os.path.join(settings.MEDIA_ROOT, 'converted_files'),
        settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else None
    ]
    
    all_good = True
    for directory in directories:
        if directory:
            if os.path.exists(directory):
                print(f"✅ Directorio existe: {directory}")
            else:
                print(f"⚠️  Directorio no existe (se creará automáticamente): {directory}")
                try:
                    os.makedirs(directory, exist_ok=True)
                    print(f"✅ Directorio creado: {directory}")
                except Exception as e:
                    print(f"❌ Error creando directorio {directory}: {e}")
                    all_good = False
    
    return all_good

def check_libreoffice():
    """Verificar LibreOffice."""
    print("\n🔍 Verificando LibreOffice...")
    
    try:
        result = subprocess.run(
            ['libreoffice', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ LibreOffice: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error ejecutando LibreOffice: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout verificando LibreOffice")
        return False
    except FileNotFoundError:
        print("❌ LibreOffice no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error inesperado con LibreOffice: {e}")
        return False

def check_python_packages():
    """Verificar paquetes de Python."""
    print("\n🔍 Verificando paquetes de Python...")
    
    required_packages = {
        'django': 'Django',
        'pdf2docx': 'pdf2docx',
        'gunicorn': 'gunicorn',
        'whitenoise': 'whitenoise'
    }
    
    all_good = True
    for package, display_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {display_name} instalado")
        except ImportError:
            print(f"❌ {display_name} NO instalado")
            all_good = False
    
    return all_good

def check_environment_variables():
    """Verificar variables de entorno importantes."""
    print("\n🔍 Verificando variables de entorno...")
    
    env_vars = {
        'PORT': os.environ.get('PORT', 'No definido'),
        'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE', 'No definido'),
        'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT', 'No definido'),
        'DEBUG': os.environ.get('DEBUG', 'No definido')
    }
    
    for var, value in env_vars.items():
        print(f"ℹ️  {var}: {value}")
    
    return True

def main():
    """Ejecutar todas las verificaciones."""
    print("🚀 Iniciando verificación completa del sistema...\n")
    
    checks = [
        ("Configuración Django", check_django_config),
        ("Directorios", check_directories),
        ("LibreOffice", check_libreoffice),
        ("Paquetes Python", check_python_packages),
        ("Variables de entorno", check_environment_variables)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en verificación de {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE VERIFICACIONES:")
    print("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡Todas las verificaciones pasaron! El sistema está listo.")
        return 0
    else:
        print("\n⚠️  Algunas verificaciones fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())