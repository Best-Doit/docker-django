import os
import subprocess
import mimetypes
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

@csrf_protect
@require_http_methods(["GET", "POST"])
def convertir_word_pdf(request):
    message = None
    archivo_pdf = None
    
    if request.method == 'POST' and request.FILES.get('word_file'):
        word_file = request.FILES['word_file']
        
        # Validar tamaño del archivo
        if word_file.size > settings.MAX_UPLOAD_SIZE:
            message = f"El archivo es demasiado grande. Máximo permitido: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
            return render(request, 'index.html', {'message': message})
        
        # Validar extensión del archivo
        file_extension = os.path.splitext(word_file.name)[1].lower()
        if file_extension not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            message = f"Tipo de archivo no permitido. Solo se permiten: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}"
            return render(request, 'index.html', {'message': message})
        
        # Validar tipo MIME
        mime_type, _ = mimetypes.guess_type(word_file.name)
        allowed_mimes = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                        'application/msword']
        if mime_type not in allowed_mimes:
            message = "Tipo de archivo no válido. Solo se permiten documentos de Word."
            return render(request, 'index.html', {'message': message})
        
        # Directorio donde se guardará el archivo
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_files')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)

        # Sanitizar nombre del archivo
        safe_filename = ''.join(c for c in word_file.name if c.isalnum() or c in '._-')
        if not safe_filename:
            safe_filename = 'documento.docx'
        
        # Guardar el archivo DOCX
        filename = fs.save(safe_filename, word_file)
        filepath = os.path.join(upload_dir, filename)

        # Definir la ruta de salida del PDF
        pdf_filename = os.path.splitext(filename)[0] + '.pdf'
        pdf_path = os.path.join(upload_dir, pdf_filename)

        try:
            # Convertir DOCX a PDF usando LibreOffice en modo headless
            subprocess.run(
                ['libreoffice', '--headless', '--convert-to', 'pdf', filepath, '--outdir', upload_dir],
                check=True
            )
            
            # Eliminar el archivo DOCX después de la conversión
            os.remove(filepath)

            archivo_pdf = pdf_filename
            message = f"¡Se ha convertido {word_file.name} a {archivo_pdf} exitosamente!"
        except subprocess.CalledProcessError as e:
            message = f"Error en la conversión: {e}"

    return render(request, 'index.html', {'message': message, 'archivo_pdf': archivo_pdf})


@require_http_methods(["GET"])
def descargar_pdf(request, filename):
    """Permite descargar el archivo PDF generado."""
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', filename)

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponseNotFound('El archivo PDF no se encontró')
