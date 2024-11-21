from PyPDF2 import PdfReader

def convert_pdf_to_txt(pdf_path, txt_path):
    try:
        # Charger le fichier PDF
        reader = PdfReader(pdf_path)
        
        # Ouvrir le fichier texte en mode écriture
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for page_num, page in enumerate(reader.pages, start=1):
                # Écrire une séparation entre les pages
                txt_file.write(f"=== Page {page_num} ===\n")
                
                # Extraire le texte de la page
                texte = page.extract_text()
                if texte:
                    txt_file.write(texte.strip() + "\n")
                else:
                    txt_file.write("[Page vide ou non lisible]\n")
                
                # Ajouter une ligne vide entre les pages pour lisibilité
                txt_file.write("\n")
        
        print(f"Conversion réussie ! Le fichier texte a été enregistré sous : {txt_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")