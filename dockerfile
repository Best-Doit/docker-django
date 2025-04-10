FROM python:3.9-bullseye-slim

# Instalar LibreOffice y dependencias necesarias
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-core \
    libreoffice-common \
    libreoffice-calc \
    fonts-dejavu \
    && apt-get clean

# Instalar dependencias de Python
RUN pip install --upgrade pip

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código fuente
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto 8000
EXPOSE 8000

# Define el comando para ejecutar la aplicación con gunicorn (más adecuado para producción)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]

