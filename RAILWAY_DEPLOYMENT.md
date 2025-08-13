# 🚀 Despliegue en Railway

Esta guía te ayudará a desplegar la aplicación de conversión de documentos en Railway.

## 📋 Prerrequisitos

1. Cuenta en [Railway](https://railway.app/)
2. CLI de Railway instalado (opcional)
3. Repositorio Git con el código

## 🔧 Configuración

### 1. Variables de Entorno en Railway

Configura las siguientes variables de entorno en tu proyecto de Railway:

```bash
# Obligatorias
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.railway.app,*.up.railway.app
RAILWAY_ENVIRONMENT=production
PORT=8000

# Opcionales para mayor seguridad
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_USE_HTTPS=True
```

### 2. Generar SECRET_KEY

Para generar una nueva SECRET_KEY segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🚀 Métodos de Despliegue

### Método 1: Desde GitHub (Recomendado)

1. Sube tu código a GitHub
2. Ve a [Railway](https://railway.app/)
3. Crea un nuevo proyecto
4. Conecta tu repositorio de GitHub
5. Railway detectará automáticamente el `Dockerfile`
6. Configura las variables de entorno
7. ¡Despliega!

### Método 2: Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Configurar variables de entorno
railway variables set DJANGO_SECRET_KEY=tu-clave-secreta
railway variables set DJANGO_DEBUG=False
railway variables set RAILWAY_ENVIRONMENT=production

# Desplegar
railway up
```

## 📁 Archivos de Configuración

La aplicación incluye los siguientes archivos para Railway:

- `railway.toml` - Configuración principal de Railway
- `Procfile` - Comandos de ejecución
- `dockerfile` - Imagen Docker optimizada
- `.railwayignore` - Archivos a excluir del despliegue
- `.env.example` - Variables de entorno de ejemplo

## 🔍 Verificación del Despliegue

1. **Salud de la aplicación**: Railway proporcionará una URL como `https://tu-app.up.railway.app`
2. **Logs**: Revisa los logs en el dashboard de Railway
3. **Funcionalidad**: Prueba la conversión de documentos

## 🛠️ Solución de Problemas

### Error: "Application failed to respond"
- Verifica que `PORT` esté configurado correctamente
- Revisa los logs para errores específicos

### Error: "Static files not found"
- Railway ejecuta automáticamente `collectstatic`
- Verifica la configuración de `STATIC_ROOT` en `settings.py`

### Error: "Secret key not set"
- Configura `DJANGO_SECRET_KEY` en las variables de entorno

## 📊 Recursos Recomendados

- **Memoria**: 512Mi (configurado en `railway.toml`)
- **CPU**: 500m (configurado en `railway.toml`)
- **Réplicas**: 1-3 (auto-scaling configurado)

## 🔒 Seguridad

La aplicación incluye:
- HTTPS automático en Railway
- Validación de tipos MIME
- Límites de tamaño de archivo (10MB)
- Headers de seguridad configurados
- CSRF protection habilitado

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Railway
2. Verifica las variables de entorno
3. Consulta la documentación de Railway

¡Tu aplicación de conversión de documentos estará lista en minutos! 🎉