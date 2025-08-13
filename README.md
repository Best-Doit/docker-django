# Docs PDF - Conversor de Documentos Word a PDF

Aplicación Django para convertir documentos Word (.docx) a PDF utilizando LibreOffice en un entorno containerizado.

## 🚀 Características

- Conversión de archivos DOCX a PDF
- Interfaz web intuitiva
- Descarga automática de archivos convertidos
- Arquitectura basada en microservicios con Docker
- Base de datos PostgreSQL
- Cache con Redis
- Proxy reverso con Nginx
- Configuración lista para producción

## 🛠️ Tecnologías

- **Backend**: Django 4.2
- **Base de datos**: PostgreSQL 15
- **Cache**: Redis 7
- **Servidor web**: Nginx
- **Servidor de aplicación**: Gunicorn
- **Containerización**: Docker & Docker Compose
- **Conversión**: LibreOffice (modo headless)

## 📋 Requisitos

- Docker
- Docker Compose
- Git

## 🚀 Instalación y Despliegue

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd docs_pdf
```

### 2. Configurar variables de entorno

Crea o modifica el archivo `.env`:

```env
DJANGO_SECRET_KEY=tu_clave_secreta_aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tu-dominio.com,localhost,127.0.0.1
DB_NAME=docs_pdf_db
DB_USER=postgres
DB_PASSWORD=tu_password_seguro
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
```

### 3. Construir y ejecutar con Docker Compose

```bash
# Construir las imágenes
docker-compose build

# Ejecutar en modo desarrollo
docker-compose up

# Ejecutar en modo producción (en segundo plano)
docker-compose up -d
```

### 4. Acceder a la aplicación

- **Aplicación web**: http://localhost
- **Panel de administración**: http://localhost/admin
  - Usuario: `admin`
  - Contraseña: `admin123`

## 🔧 Comandos útiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs

# Servicio específico
docker-compose logs web
docker-compose logs db
docker-compose logs redis
docker-compose logs nginx
```

### Ejecutar comandos Django
```bash
# Migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Recopilar archivos estáticos
docker-compose exec web python manage.py collectstatic

# Shell de Django
docker-compose exec web python manage.py shell
```

### Gestión de contenedores
```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir servicios
docker-compose up --build

# Ver estado de servicios
docker-compose ps
```

## 📁 Estructura del proyecto

```
docs_pdf/
├── app_main/                 # Configuración principal de Django
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── docs_pdf/                # Aplicación principal
│   ├── views.py             # Lógica de conversión
│   ├── urls.py              # URLs de la app
│   └── templates/           # Plantillas HTML
├── staticfiles/             # Archivos estáticos recopilados
├── media/                   # Archivos subidos y generados
├── dockerfile               # Configuración de Docker
├── docker-compose.yml       # Orquestación de servicios
├── nginx.conf              # Configuración de Nginx
├── entrypoint.sh           # Script de inicialización
├── requirements.txt        # Dependencias Python
├── .dockerignore          # Archivos excluidos de Docker
└── .env                   # Variables de entorno
```

## 🔒 Configuración de Seguridad

La aplicación incluye configuraciones de seguridad para producción:

- HTTPS redirect (cuando SSL está configurado)
- Headers de seguridad
- Configuración CORS
- Validación CSRF
- Configuración de cookies seguras

### Configurar HTTPS (Opcional)

1. Obtén certificados SSL
2. Colócalos en el directorio `ssl/`
3. Descomenta la configuración HTTPS en `nginx.conf`
4. Actualiza las variables de entorno para HTTPS

## 📊 Monitoreo y Logs

Los logs se almacenan en:
- **Django**: `/app/django.log` (dentro del contenedor)
- **Nginx**: Logs estándar de Docker
- **PostgreSQL**: Logs estándar de Docker
- **Redis**: Logs estándar de Docker

## 🐛 Solución de problemas

### Error de conexión a la base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
docker-compose ps db

# Ver logs de la base de datos
docker-compose logs db
```

### Error de LibreOffice
```bash
# Verificar que LibreOffice esté instalado en el contenedor
docker-compose exec web libreoffice --version
```

### Problemas de permisos
```bash
# Verificar permisos de archivos
docker-compose exec web ls -la /app/media/
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas, por favor abre un issue en el repositorio.

---

**Nota**: Asegúrate de cambiar las credenciales por defecto antes de desplegar en producción.