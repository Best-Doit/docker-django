# Imagen base ligera
FROM python:3.11-slim

# Evitar que Python genere .pyc y usar buffer estándar
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para pdf2docx
RUN apt-get update && apt-get install -y \
    libmagic1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Colectar estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto (Railway usa variable PORT)
EXPOSE $PORT

# Comando para producción con Railway
CMD gunicorn app_main.wsgi:application --bind 0.0.0.0:$PORT
