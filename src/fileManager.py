import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # Éviter les dossiers
            print(f"Fichier créé : {event.src_path}")
        else:
            print(f"Nouveau dossier : {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:  # Éviter les dossiers
            print(f"Fichier supprimé : {event.src_path}")
        else:
            print(f"Dossier supprimé : {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:  # Éviter les dossiers
            print(f"Fichier modifié : {event.src_path}")
        else:
            print(f"Dossier modifié : {event.src_path}")

    def on_moved(self, event):
        print(f"Déplacé : {event.src_path} -> {event.dest_path}")

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
