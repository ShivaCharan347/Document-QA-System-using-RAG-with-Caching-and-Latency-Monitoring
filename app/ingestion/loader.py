import os
from PyPDF2 import PdfReader

class DocumentLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        
    def load(self):
        docs = []
        if not os.path.exists(self.data_path):
            return docs
            
        for f in os.listdir(self.data_path):
            path = os.path.join(self.data_path, f)
            if f.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as file:
                    docs.append({"source": f, "text": file.read()})
            elif f.endswith(".pdf"):
                text = ""
                with open(path, "rb") as file:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted: text += extracted + "\n"
                docs.append({"source": f, "text": text})
        return docs
