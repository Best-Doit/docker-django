import os
import subprocess
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def convertir_a_pdf(input_path, output_path):
    """Convierte un archivo DOCX a PDF usando unoconv."""
    try:
        subprocess.run(["unoconv", "-f", "pdf", "-o", output_path, input_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return f"Error en la conversión: {str(e)}"

import os
import subprocess
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def convertir_word_pdf(request):
    message = None
    archivo_pdf = None
    
    if request.method == 'POST' and request.FILES.get('word_file'):
        word_file = request.FILES['word_file']
        
        # Directorio donde se guardará el archivo
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_files')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)

        # Guardar el archivo DOCX
        filename = fs.save(word_file.name, word_file)
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
