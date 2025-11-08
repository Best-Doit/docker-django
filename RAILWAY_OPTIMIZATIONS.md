# Railway Deployment Guide - Conversión de Documentos

## 🚀 Optimizaciones Implementadas para Railway

### 1. **Archivos Estáticos Agregados**
- ✅ `robots.txt` - Elimina warnings de robots.txt
- ✅ `favicon.ico` - Elimina warnings de favicon

### 2. **Configuración de Railway Optimizada**
- **Memoria optimizada**: 512Mi (suficiente para conversión de documentos)
- **CPU**: 1000m (adecuado para LibreOffice)
- **Healthcheck mejorado**: Intervalo de 90s, timeout 60s
- **Replicas**: Máximo 2

### 3. **Código Compatible con Railway**
- **Conversión Word ↔ PDF**: Usando LibreOffice y pdf2docx
- **Soporte múltiples formatos**: .docx, .doc, .pdf, .odt, .rtf
- **Mejor manejo de errores**: Logs más informativos

### 4. **Dependencias Optimizadas**
- **LibreOffice**: Para conversión de documentos a PDF
- **pdf2docx**: Para conversión de PDF a Word
- **Django**: Framework web ligero

## 🔧 **Problemas Solucionados**

### Warnings Eliminados:
- ❌ `[WARNING] Not Found: /robots.txt` → ✅ Archivo creado
- ❌ `[WARNING] Not Found: /favicon.ico` → ✅ Archivo creado

### Recursos Optimizados:
- **Memoria reducida**: Ya no necesitamos recursos para OCR
- **CPU adecuada**: Suficiente para LibreOffice
- **Healthcheck configurado**: Monitoreo adecuado

## 📊 **Configuración Final**

### Railway.toml:
```toml
[resources]
memory = "512Mi"      # Optimizado para conversión de documentos
cpu = "1000m"         # Adecuado para LibreOffice

[healthcheck]
interval = 90         # Intervalo de verificación
timeout = 60         # Timeout para conversiones
```

### Dockerfile:
- ✅ LibreOffice instalado para conversiones
- ✅ Dependencias mínimas necesarias
- ✅ Imagen optimizada y ligera

## 🎯 **Formatos Soportados**

### Entrada:
- `.docx` - Microsoft Word (formato moderno)
- `.doc` - Microsoft Word (formato antiguo)
- `.odt` - OpenDocument Text
- `.rtf` - Rich Text Format
- `.pdf` - Portable Document Format

### Salida:
- `.pdf` - Desde documentos Word/Office
- `.docx` - Desde archivos PDF

## 🚨 **Notas Importantes**

- **LibreOffice**: Requerido para conversión a PDF
- **pdf2docx**: Requerido para conversión de PDF a Word
- **Memoria**: 512Mi es suficiente para la mayoría de documentos
- **Timeout**: 60 segundos para conversiones largas

¡Tu aplicación está optimizada para Railway! 🚀
