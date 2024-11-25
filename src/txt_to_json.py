import json

def convert_txt_to_json(txt_path, json_path):
    try:
        # Lire le contenu du fichier texte
        with open(txt_path, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read().strip()  # Lire tout le fichier et retirer les espaces inutiles
        
        # Construire le format JSON
        pages = [{
            "page_number": 1,
            "content": content if content else "[Document vide]"
        }]
        
        # Sauvegarder le contenu dans un fichier JSON
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(pages, json_file, indent=4, ensure_ascii=False)
        
        print(f"Conversion réussie ! Le fichier JSON a été enregistré sous : {json_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
