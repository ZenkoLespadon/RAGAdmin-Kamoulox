import os
from PyPDF2 import PdfReader
from typing import Any


def convert_pdf_in_txt(source_path: str, save_path: str) -> None:
    """
    Convertit un fichier PDF en fichier texte en extrayant le contenu de chaque page.

    Cette fonction lit un fichier PDF spécifié par `source_path`, extrait le texte de chaque
    page et l'enregistre dans un fichier texte à l'emplacement `save_path`.

    Args:
        source_path (str): Chemin d'accès au fichier PDF source.
        save_path (str): Chemin où enregistrer le fichier texte généré.

    Raises:
        FileNotFoundError: Si le fichier PDF source n'existe pas.
        IOError: En cas de problème lors de l'écriture du fichier texte.
        Exception: Pour toute autre erreur inattendue.

    Example:
        convert_pdf_in_txt("document.pdf", "document.txt")
    """
    # Typage explicite des variables
    source_path: str
    save_path: str
    reader: PdfReader
    txt_file: Any
    texte: str
    page_num: int
    page: Any
    if not os.access(source_path, os.R_OK):
        print(f"Erreur : Impossible de lire le fichier source {source_path}. Vérifiez les permissions.")
        return

    if not os.access(os.path.dirname(save_path) or ".", os.W_OK):
        print(f"Erreur : Impossible d'écrire dans le dossier de destination {os.path.dirname(save_path)}.")
        return

    try:
        # Charger le fichier PDF
        reader = PdfReader(source_path)

        # Ouvrir le fichier texte en mode écriture
        with open(save_path, 'w', encoding='utf-8') as txt_file:
            for page_num, page in enumerate(reader.pages, start=1):
                # Extraire le texte de la page
                texte = page.extract_text()
                if texte:
                    txt_file.write(texte.strip() + "\n")

                # Ajouter une ligne vide entre les pages pour lisibilité
                txt_file.write("\n")

        print(f"Conversion réussie ! Le fichier texte a été enregistré sous : {save_path}")
    except Exception as e:
        e: Exception  # Exception capturée
        print(f"Erreur lors de la conversion : {e}")



