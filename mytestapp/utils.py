import PyPDF2
import os
from django.conf import settings

def extract_text_from_predefined_pdf():
    pdf_path = os.path.join(settings.BASE_DIR, 'mytestapp/static/mytestapp/pdfs/gakuseibinran20241.pdf')
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text
