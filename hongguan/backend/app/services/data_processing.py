import os
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
from PIL import Image
import pytesseract

class DataProcessor:
    def __init__(self):
        self.upload_folder = 'uploaded_files'
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def save_file(self, filename, contents):
        safe_filename = self.secure_filename(filename)
        file_path = os.path.join(self.upload_folder, safe_filename)
        with open(file_path, 'wb') as f:
            f.write(contents)
        return file_path

    def secure_filename(self, filename):
        return os.path.basename(filename)
    
    def extract_text(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension == '.pdf':
            return self._extract_text_from_pdf(file_path)
        elif extension in ['.doc', '.docx']:
            return self._extract_text_from_word(file_path)
        elif extension in ['.xls', '.xlsx']:
            return self._extract_text_from_excel(file_path)
        elif extension in ['.png', '.jpg', '.jpeg']:
            return self._extract_text_from_image(file_path)
        else:
            raise ValueError("不支持的文件类型")

    def _extract_text_from_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    def _extract_text_from_word(self, file_path):
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text

    def _extract_text_from_excel(self, file_path):
        df = pd.read_excel(file_path)
        text = df.to_csv(index=False)
        return text

    def _extract_text_from_image(self, file_path):
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
