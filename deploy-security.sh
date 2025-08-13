#!/bin/bash

# Script de despliegue seguro para docs-pdf
# Ejecutar con: bash deploy-security.sh

set -e  # Salir si cualquier comando falla

echo "🔒 Iniciando despliegue seguro de docs-pdf..."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encontró manage.py. Ejecuta este script desde el directorio del proyecto."
    exit 1
fi

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encontró el archivo .env. Copia .env.example a .env y configúralo."
    exit 1
fi

# Verificar configuraciones críticas de seguridad
echo "🔍 Verificando configuraciones de seguridad..."

# Verificar que DEBUG esté en False
if grep -q "DJANGO_DEBUG=True" .env; then
    echo "⚠️  ADVERTENCIA: DEBUG está habilitado en .env. Cambiando a False..."
    sed -i 's/DJANGO_DEBUG=True/DJANGO_DEBUG=False/g' .env
fi

# Verificar que SECRET_KEY no sea la por defecto
if grep -q "django-insecure" .env; then
    echo "❌ Error: Estás usando una SECRET_KEY insegura. Genera una nueva."
    echo "Ejecuta: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
    exit 1
fi

# Verificar que ALLOWED_HOSTS esté configurado correctamente
if grep -q "tu-dominio.com" .env; then
    echo "⚠️  ADVERTENCIA: ALLOWED_HOSTS contiene 'tu-dominio.com'. Asegúrate de cambiarlo por tu dominio real."
fi

# Crear directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p staticfiles media/pdf_files ssl

# Establecer permisos seguros
echo "🔐 Configurando permisos seguros..."
chmod 755 staticfiles media
chmod 644 .env
chmod 600 ssl/* 2>/dev/null || true

# Construir imagen Docker
echo "🐳 Construyendo imagen Docker..."
docker build -t docs-pdf:latest .

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Ejecutar verificaciones de seguridad en la imagen
echo "🔍 Ejecutando verificaciones de seguridad..."

# Verificar que no se ejecute como root
if docker run --rm docs-pdf:latest whoami | grep -q "root"; then
    echo "❌ Error: La aplicación se ejecuta como root. Esto es un riesgo de seguridad."
    exit 1
fi

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar que los servicios estén funcionando
echo "✅ Verificando servicios..."
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ Servicios iniciados correctamente"
else
    echo "❌ Error: Los servicios no se iniciaron correctamente"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

# Mostrar estado final
echo ""
echo "🎉 ¡Despliegue completado!"
echo ""
echo "📊 Estado de los servicios:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "📝 Recordatorios de seguridad:"
echo "   • Configura certificados SSL en el directorio ./ssl/"
echo "   • Actualiza ALLOWED_HOSTS con tu dominio real"
echo "   • Configura un firewall para limitar acceso a puertos"
echo "   • Implementa monitoreo y logs de seguridad"
echo "   • Realiza backups regulares"
echo "   • Mantén Docker y dependencias actualizadas"
echo ""
echo "🌐 Aplicación disponible en: http://localhost (o tu dominio configurado)"