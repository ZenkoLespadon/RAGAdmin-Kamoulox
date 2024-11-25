import json
from PyPDF2 import PdfReader

def convert_pdf_to_json(pdf_path, json_path):
    try:
        # Charger le fichier PDF
        reader = PdfReader(pdf_path)
        pages = []
        
        # Extraire le contenu de chaque page
        for page_num, page in enumerate(reader.pages, start=1):
            texte = page.extract_text()
            pages.append({
                "page_number": page_num,
                "content": texte.strip() if texte else "[Page vide ou non lisible]"
            })
        
        # Enregistrer dans un fichier JSON
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(pages, json_file, indent=4, ensure_ascii=False)
        
        print(f"Conversion réussie ! Le fichier JSON a été enregistré sous : {json_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
