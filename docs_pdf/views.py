import os
import subprocess
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from pdf2docx import Converter


@csrf_protect
@require_http_methods(["GET", "POST"])
def convertir_documento(request):
    message = None
    archivo_convertido = None
    
    if request.method == 'POST' and request.FILES.get('document_file'):
        document_file = request.FILES['document_file']
        
        # Validar tamaño del archivo
        if document_file.size > settings.MAX_UPLOAD_SIZE:
            message = f"El archivo es demasiado grande. Máximo permitido: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
            return render(request, 'index.html', {'message': message})
        
        # Validar extensión del archivo
        file_extension = os.path.splitext(document_file.name)[1].lower()
        if file_extension not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            message = f"Tipo de archivo no permitido. Solo se permiten: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}"
            return render(request, 'index.html', {'message': message})
        
        # Directorio donde se guardará el archivo
        try:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'converted_files')
            os.makedirs(upload_dir, exist_ok=True)
            fs = FileSystemStorage(location=upload_dir)
        except Exception as e:
            message = f"Error al crear directorio de carga: {e}"
            return render(request, 'index.html', {'message': message})

        # Sanitizar nombre del archivo
        safe_filename = ''.join(c for c in document_file.name if c.isalnum() or c in '._-')
        if not safe_filename:
            safe_filename = f'documento{file_extension}'
        
        # Guardar el archivo
        try:
            filename = fs.save(safe_filename, document_file)
            filepath = os.path.join(upload_dir, filename)
        except Exception as e:
            message = f"Error al guardar el archivo: {e}"
            return render(request, 'index.html', {'message': message})

        try:
            # Conversión de documentos Word/Office a PDF
            if file_extension in ['.docx', '.doc', '.odt', '.rtf']:
                # Convertir Word/Office a PDF usando LibreOffice
                output_filename = os.path.splitext(filename)[0] + '.pdf'
                result = subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', 'pdf', filepath, '--outdir', upload_dir],
                    check=True,
                    timeout=60,  # Timeout de 60 segundos
                    capture_output=True,
                    text=True
                )
                
                # Verificar que el archivo de salida se haya creado
                output_path = os.path.join(upload_dir, output_filename)
                if not os.path.exists(output_path):
                    raise Exception("LibreOffice no pudo generar el archivo PDF")
                
                conversion_type = f"Documento ({file_extension.upper()}) a PDF"

            # Conversión de PDF a Word
            elif file_extension == '.pdf':
                # Convertir PDF a Word usando pdf2docx
                output_filename = os.path.splitext(filename)[0] + '.docx'
                output_path = os.path.join(upload_dir, output_filename)
                
                try:
                    cv = Converter(filepath)
                    cv.convert(output_path, start=0, end=None)
                    cv.close()
                    conversion_type = "PDF a Word"
                except Exception as e:
                    message = f"Error al convertir PDF a Word: {e}"
                    # Limpiar archivo temporal si existe
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return render(request, 'index.html', {'message': message})
            else:
                message = f"Formato de archivo no soportado: {file_extension}"
                if os.path.exists(filepath):
                    os.remove(filepath)
                return render(request, 'index.html', {'message': message})
            
            # Eliminar el archivo original después de la conversión
            if os.path.exists(filepath):
                os.remove(filepath)

            archivo_convertido = output_filename
            message = f"¡Se ha convertido {document_file.name} de {conversion_type} exitosamente!"
            
        except subprocess.TimeoutExpired:
            message = "Error: La conversión tardó demasiado tiempo. Intenta con un archivo más pequeño."
            if os.path.exists(filepath):
                os.remove(filepath)
        except subprocess.CalledProcessError as e:
            # Incluir la salida de LibreOffice en el mensaje de error
            error_output = e.stderr if e.stderr else e.stdout
            if 'libreoffice' in str(e.cmd):
                message = f"Error: LibreOffice no pudo convertir el archivo. Verifica que el archivo no esté corrupto o sea compatible. Detalles: {error_output}"
            else:
                message = f"Error en la conversión: {e}. Detalles: {error_output}"
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            message = f"Error inesperado en la conversión: {e}"
            if os.path.exists(filepath):
                os.remove(filepath)

    return render(request, 'index.html', {'message': message, 'archivo_convertido': archivo_convertido})


@require_http_methods(["GET"])
def descargar_archivo(request, filename):
    """Permite descargar el archivo convertido (PDF o DOCX)."""
    file_path = os.path.join(settings.MEDIA_ROOT, 'converted_files', filename)

    if os.path.exists(file_path):
        # Determinar el tipo de contenido basado en la extensión
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension == '.pdf':
            content_type = 'application/pdf'
        elif file_extension == '.docx':
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:
            content_type = 'application/octet-stream'
        
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponseNotFound('El archivo convertido no se encontró')
