# Imagen base ultra ligera con solo lo esencial
FROM python:3.11-slim

# Optimizaciones de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Directorio de trabajo
WORKDIR /app

# Instalar SOLO dependencias esenciales para OCR y procesamiento
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    poppler-utils \
    libreoffice \
    libreoffice-writer \
    fonts-liberation \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements primero para mejor caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar solo lo necesario para producción
COPY app_main/ ./app_main/
COPY docs_pdf/ ./docs_pdf/
COPY manage.py .
COPY static/ ./static/

# Colectar estáticos
RUN python manage.py collectstatic --noinput

# Puerto expuesto
EXPOSE 8000

# Comando de producción optimizado
CMD ["gunicorn", "app_main.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]