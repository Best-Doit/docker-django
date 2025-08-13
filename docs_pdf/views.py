import os
import subprocess
import mimetypes
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
        
        # Validar tipo MIME según el tipo de archivo
        mime_type, _ = mimetypes.guess_type(document_file.name)
        if file_extension in ['.docx', '.doc']:
            if mime_type not in settings.ALLOWED_WORD_MIMES:
                message = "Tipo de archivo no válido. Solo se permiten documentos de Word válidos."
                return render(request, 'index.html', {'message': message})
        elif file_extension == '.pdf':
            if mime_type not in settings.ALLOWED_PDF_MIMES:
                message = "Tipo de archivo no válido. Solo se permiten archivos PDF válidos."
                return render(request, 'index.html', {'message': message})
        
        # Directorio donde se guardará el archivo
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'converted_files')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)

        # Sanitizar nombre del archivo
        safe_filename = ''.join(c for c in document_file.name if c.isalnum() or c in '._-')
        if not safe_filename:
            safe_filename = f'documento{file_extension}'
        
        # Guardar el archivo
        filename = fs.save(safe_filename, document_file)
        filepath = os.path.join(upload_dir, filename)

        try:
            if file_extension in ['.docx', '.doc']:
                # Convertir Word a PDF usando LibreOffice
                output_filename = os.path.splitext(filename)[0] + '.pdf'
                subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', 'pdf', filepath, '--outdir', upload_dir],
                    check=True
                )
                conversion_type = "Word a PDF"
            
            elif file_extension == '.pdf':
                # Convertir PDF a Word usando pdf2docx
                output_filename = os.path.splitext(filename)[0] + '.docx'
                output_path = os.path.join(upload_dir, output_filename)
                
                cv = Converter(filepath)
                cv.convert(output_path, start=0, end=None)
                cv.close()
                conversion_type = "PDF a Word"
            
            # Eliminar el archivo original después de la conversión
            os.remove(filepath)

            archivo_convertido = output_filename
            message = f"¡Se ha convertido {document_file.name} de {conversion_type} exitosamente!"
            
        except subprocess.CalledProcessError as e:
            message = f"Error en la conversión con LibreOffice: {e}"
        except Exception as e:
            message = f"Error en la conversión: {e}"

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
