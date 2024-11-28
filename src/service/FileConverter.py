import os
from PyPDF2 import PdfReader
import csv


def convert_pdf_to_txt(source_path: str, save_path: str) -> None:
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
    text: str
    page_num: int
    os.chmod(source_path, 0o777)
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
        with open(save_path, 'w', encoding='utf-8') as text_file:
            for page_num, page in enumerate(reader.pages, start=1):
                # Extraire le texte de la page
                text = page.extract_text()
                if text:
                    text_file.write(text + "\n")

                # Ajouter une ligne vide entre les pages pour lisibilité
                text_file.write("\n")

        print(f"Conversion réussie ! Le fichier texte a été enregistré sous : {save_path}")
    except Exception as e:
        e: Exception  # Exception capturée
        print(f"Erreur lors de la conversion : {e}")

def convert_csv_to_txt(source_path: str, save_path: str)->None:
    """
    Convertit un fichier CSV en fichier TXT.

    Args:
        source_path (str): Le chemin du fichier CSV à convertir.
        save_path (str): Le chemin du fichier TXT de sortie.

    Exemple:
        csv_to_txt("fichier.csv", "fichier.txt")
        Cette commande convertira le fichier "fichier.csv" en "fichier.txt".
    """
    try:
        with open(source_path, mode='r', newline='', encoding='utf-8') as csv_f:
            csv_reader = csv.reader(csv_f)
            with open(save_path, mode='w', encoding='utf-8') as txt_f:
                for row in csv_reader:
                    txt_f.write(";".join(row) + "\n")  # Utilisation de tabulation pour séparer les colonnes

        print(f"Le fichier {source_path} a été converti en {save_path}")

    except FileNotFoundError:
        print(f"Le fichier {source_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

def copy_file(source, destination):
    """
    Copie le contenu d'un fichier source vers un fichier de destination.

    Args:
        source (str): Le chemin du fichier source à copier.
        destination (str): Le chemin du fichier de destination où le contenu sera copié.

    Raises:
        FileNotFoundError: Si le fichier source n'est pas trouvé.
        Exception: Si une autre erreur se produit lors de la copie du fichier.

    Exemple:
        copy_file("source.txt", "copie.txt")
        Cette commande copiera le contenu de "source.txt" vers "copie.txt".
    """
    try:
        shutil.copy(source, destination)
        print(f"Le fichier a été copié de {source} vers {destination}")
    except FileNotFoundError:
        print("Le fichier source n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")