from django.shortcuts import render
from PyPDF2 import PdfMerger
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from datetime import datetime

def merge_pdfs(request):
    merged_file_url = None

    if request.method == 'POST':
        pdf_files = request.FILES.getlist('pdfs')
        merger = PdfMerger()
        fs = FileSystemStorage()

        file_paths = []

        for pdf in pdf_files:
            filename = fs.save(pdf.name, pdf)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            file_paths.append(file_path)
            merger.append(file_path)

        output_filename = f'merged_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
        output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

        with open(output_path, 'wb') as f_out:
            merger.write(f_out)

        merger.close()

        # Delete temp files
        for path in file_paths:
            os.remove(path)

        merged_file_url = settings.MEDIA_URL + output_filename

    return render(request, 'merger/merge.html', {'merged_file_url': merged_file_url})
