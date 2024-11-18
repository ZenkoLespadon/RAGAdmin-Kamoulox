import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def file_or_folder(path:str) -> str :
    """
        Fonction qui prend en paramette un chemin d'accès et différentie un fichier d'un dossier

        Entrée : path

        Sortie : folder  -  type d'objet désigné
              ou file
              ou unknow
    """
    # Vérifier si le chemin est un dossier
    if os.path.isdir(path):
        return "folder"
    # Vérifier si le chemin est un fichier
    if os.path.isfile(path):
        return "file"
    return "unknow"

def create_missing_directories(path: str) -> None:
    """
    Crée tous les répertoires manquants dans le chemin donné.

    Entrée: path - Le chemin d'accès pour lequel les répertoires manquants doivent être créés.
    Sortie: None

    """

    path = os.path.normpath(path)
    folder_path = Path(os.path.dirname(path))
    folder_path.mkdir(parents=True, exist_ok=True)

def replace_first_folder(path:str,file_name:str) -> str :
    """
        Fonction qui remplace le premier dossier d'un chemin d'accès par un autre
        Entrée: path - Le chemin d'accès original.
        Sortie: path - nouveau chemin.
    """
    path = os.path.normpath(path)
    dossiers = path.split(os.sep)

    if dossiers[0] != ".":
        dossiers[0] = file_name
    return os.path.join(*dossiers)

def get_file_extension(filename):
    """
    Renvoie l'extension d'un fichier.

    Args:
        filename (str): Le nom du fichier ou son chemin complet.

    Returns:
        str: L'extension du fichier (par exemple '.txt'), ou une chaîne vide si aucune extension.
    """
    _, extension = os.path.splitext(filename)
    return extension

def replace_extension_with_txt(file_path):
    """
    Remplace l'extension d'un fichier par '.txt'.

    Args:
        file_path (str): Chemin d'accès au fichier.

    Returns:
        str: Nouveau chemin avec l'extension '.txt'.
    """
    base_name, _ = os.path.splitext(file_path)
    new_path = f"{base_name}.txt"
    return new_path

class MyHandler(FileSystemEventHandler):
    """
    Classe qui hérite de FileSystemEventHandler et qui redéfinit les méthodes on_created et on_deleted

    Entrée (str): mirror_folder - le path du dossier miroir
    Sortie : None

    """
    def __init__(self,mirror_folder):
        self.mirror_folder=mirror_folder


    def on_created(self, event):
        path = os.path.normpath(event.src_path)
        if file_or_folder(path) == "file":  # Éviter les dossiers


            mirror_path = replace_first_folder(path,self.mirror_folder)
            #file_name = Path(mirror_path).name

            create_missing_directories(mirror_path)

            # A changer avec la fonction de convertion de pdf
            # ######################################
            mirror_path = replace_extension_with_txt(mirror_path)

            new_txt_file = Path(mirror_path)
            if new_txt_file.is_file():
                #print("le fichier existe déjà")
                pass
            else:
                with open(mirror_path, 'w') as new_file:
                    # Crée un fichier vide
                    new_file.write("")

            extension=get_file_extension(path)
            match extension:
                case ".pdf":
                    print("Conversion du pdf en txt...")
                case ".csv":
                    print("Conversion du csv en txt...")
                case ".txt":
                    print("Copie du txt...")
                case _:
                    print(f"Extension de fichier \"{extension}\" inconnue.")



                #print(f"Fichier créé : ", path)

            # ######################################
        elif file_or_folder(path) == "folder":
            #print(f"Dossier créé : ", path)
            mirror_path = replace_first_folder(path,self.mirror_folder)
            #print(mirror_path)
            create_missing_directories(mirror_path)

        else:
            print("Objet créé inconnu")

    def on_deleted(self, event):
        path = os.path.normpath(event.src_path)

        mirror_path = replace_first_folder(path,self.mirror_folder)
        file = Path(mirror_path)

        if file.is_file():
            #print(f"Le fichier '{file}' existe.")
            os.remove(mirror_path)
        else:
            if os.path.isdir(mirror_path):# si le dossier existe

                if not os.listdir(mirror_path): #si le dossier est vide
                    os.rmdir(mirror_path)
                else:                          #si le dossier est rempli
                    shutil.rmtree(mirror_path)
            else:
                print(f"Le dossier '{file}' n'existe pas.")


if __name__ == "__main__" :

    # Dossier à surveiller
    PATH_TO_WATCH = "docs"  # Remplacez par le chemin du dossier que vous voulez surveiller
    PATH_TO_SAVE = "files"

    # Initialiser l'observateur
    event_handler = MyHandler(PATH_TO_SAVE)
    observer = Observer()

    # Activer la surveillance récursive
    observer.schedule(event_handler, path=PATH_TO_WATCH, recursive=True)
    try:
        print(f"Surveillance du dossier (et sous-dossiers) : {PATH_TO_WATCH}")
        observer.start()
        while True:
            time.sleep(1)  # Garder le script actif
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
