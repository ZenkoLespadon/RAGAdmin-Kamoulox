# Lancer le projet

## La première fois

### Créer un environnement virtuel python
python3 -m venv llm-env

### Installer toutes les dépendances
pip install -r requirement.txt

### Aller dans l'environnement virtuel (à faire à la racine du projet)
source llm-env/bin/activate

### Démarrer le projet avec uvicorn (à faire à la racine du projet)
uvicorn src.__main__:app --host IP_DU_SERVEUR --port PORT_DU_SERVICE


## Les fois suivantes

### Aller dans l'environnement virtuel (à faire à la racine du projet)
source llm-env/bin/activate

### Démarrer le projet avec uvicorn (à faire à la racine du projet)
uvicorn src.__main__:app --host IP_DU_SERVEUR --port PORT_DU_SERVICE



# Ajouter un document dans ChromaDB 

### Mettre le document dans src/service/chromadb (obligatoire)

### Mettre le nom du document à la fin du fichier AddPdfToChroma.py

### Aller dans l'environnement virtuel (à faire dans src/service/chromadb ou changer le chemin)
source ../../../llm-env/bin/activate

### Lancer le programme
python3 AddPdfToChroma.py