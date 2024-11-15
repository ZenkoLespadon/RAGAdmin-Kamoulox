import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil

def fileOrFolder(path:str) -> str :
    """
        Fonction qui prend en paramette un chemin d'accès
    """
# Vérifier si le chemin est un dossier
    if os.path.isdir(path):
        #print(f"{path} est un dossier.")
        return "folder"
    # Vérifier si le chemin est un fichier
    elif os.path.isfile(path):
        #print(f"{path} est un fichier.")
        return "file"
    else:
        #print(f"{path} n'est ni un fichier ni un dossier.")
        return "unknow"



def create_missing_directories(path: str) -> None:
    """
    Crée tous les répertoires manquants dans le chemin donné.

    :param path: Le chemin d'accès pour lequel les répertoires manquants doivent être créés.
    """

    path = os.path.normpath(path)
    folderPath = Path(os.path.dirname(path))
    folderPath.mkdir(parents=True, exist_ok=True)

def replaceFirstFolder(path:str,fileName:str) -> str :
    path = os.path.normpath(path)
    dossiers = path.split(os.sep)
    print(len(dossiers))

    if dossiers[0] != ".":
        dossiers[0] = fileName
    return os.path.join(*dossiers)

class MyHandler(FileSystemEventHandler):

    def __init__(self,mirrorFolder):
        self.mirrorFolder=mirrorFolder


    def on_created(self, event):
        path = os.path.normpath(event.src_path)
        if fileOrFolder(path) == "file":  # Éviter les dossiers


            mirrorPath = replaceFirstFolder(path,self.mirrorFolder)
            fileName = Path(mirrorPath).name

            create_missing_directories(mirrorPath)

            # A changer avec la fonction de convertion de pdf
            # ######################################
            file = Path(mirrorPath)
            if file.is_file():
                print("le fichier existe déjà")
            else:
                with open(mirrorPath, 'w') as newFile:
                    newFile.write("")  # Crée un fichier vide

                print(f"Fichier créé : ", path)

            # ######################################
        elif fileOrFolder(path) == "folder":
            print(f"Dossier créé : ", path)
            mirrorPath = replaceFirstFolder(path,self.mirrorFolder)
            print(mirrorPath)
            create_missing_directories(mirrorPath)

        else:
            print(f"Objet créé inconnu")

    def on_deleted(self, event):
        path = os.path.normpath(event.src_path)

        mirrorPath = replaceFirstFolder(path,self.mirrorFolder)
        file = Path(mirrorPath)

        if file.is_file():
            print(f"Le fichier '{file}' existe.")
            os.remove(mirrorPath)
        else:
            if os.path.isdir(mirrorPath):# si le dossier existe

                if not os.listdir(mirrorPath): #si le dossier est vide
                    os.rmdir(mirrorPath)
                else:                          #si le dossier est rempli
                    shutil.rmtree(mirrorPath)
            else:
                print(f"Le dossier '{file}' n'existe pas.")





if __name__ == "__main__" :

    # Dossier à surveiller
    path_to_watch = "docs"  # Remplacez par le chemin du dossier que vous voulez surveiller
    path_to_record = "files"

    # Initialiser l'observateur
    event_handler = MyHandler(path_to_record)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)  # Activer la surveillance récursive

    try:
        print(f"Surveillance du dossier (et sous-dossiers) : {path_to_watch}")
        observer.start()
        while True:
            time.sleep(1)  # Garder le script actif
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
