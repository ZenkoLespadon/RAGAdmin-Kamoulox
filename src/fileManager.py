import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def replace_backslashes(input_str: str) -> str:
    # Remplacer tous les antislashs par des slashs
    result = ""
    for letter in input_str:
        if letter == "\\" :
            result += "/"
        else:
            result += letter
    return result

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

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        path = r"" + replace_backslashes(event.src_path)
        if fileOrFolder(path) == "file":  # Éviter les dossiers
            print(f"Fichier créé : ", replace_backslashes(path))
        elif fileOrFolder(path) == "folder":
            print(f"Dossier créé : ", replace_backslashes(path))
        else:
            print(f"Objet créé inconnu")

    def on_deleted(self, event):
        path = r"" + replace_backslashes(event.src_path)
        print(f"Objet supprimé : ",replace_backslashes(path))

    #def on_modified(self, event):
    #    path = r"" + replace_backslashes(event.src_path)
    #    if fileOrFolder(path) == "file":  # Éviter les dossiers
    #        print(f"Fichier modifié : ", replace_backslashes(path))
    #    elif fileOrFolder(path) == "folder":
    #        print(f"Dossier modifié : ", replace_backslashes(path))
    #    else:
    #        print(f"Objet modifié inconnu")


if __name__ == "__main__" :

    # Dossier à surveiller
    path_to_watch = "./files"  # Remplacez par le chemin du dossier que vous voulez surveiller

    # Initialiser l'observateur
    event_handler = MyHandler()
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
