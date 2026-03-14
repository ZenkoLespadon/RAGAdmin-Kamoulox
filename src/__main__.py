from fastapi import FastAPI, Body
import sys
from pathlib import Path
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Ajouter le dossier 'src' à sys.path
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent / "service" / "controller"))
sys.path.append(str(Path(__file__).resolve().parent / "llm"))

from src.service.chromadb.vector_store_service import *


from src.service.controller.Models import RequestAPI

# Importer les modules
from src.service.controller.handling_request import handling_request

# Définir le chemin vers le modèle
modelPath = "./Meta-Llama-3.1-8B-Instruct"

# Créer l'application FastAPI
app = FastAPI()

# Ajouter le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajouter les domaines autorisÃ©s
    allow_credentials=True,
    allow_methods=["*"],  # Permettre toutes les mÃ©thodes (GET, POST, etc.)
    allow_headers=["*"],  # Permettre tous les en-tÃªtes
)

@app.get("/")
def index():
    """
    Endpoint racine : retourne un message de bienvenue.
    """
    return {"data": "Bonjour, bienvenu sur RAGAdmin !"}

@app.post("/request/")
def requete(req: RequestAPI):

    # Définir le chemin du modèle et charger l'embedding function
    vector_store_service = VectorStoreService()

    # Afficher le nombre de documents dans la base
    print("Nombre de documents :", vector_store_service.get_document_count())

    context = vector_store_service.search_documents(req.req)
    print(req.req, "\n", context)

    """
    Endpoint POST pour traiter une requête donnée.

    Arguments:
    - req : la requête (question) à envoyer au modèle.

    Retourne:
    - La réponse générée par le modèle.
    """
    try:
        response = handling_request(req.req, modelPath, context)
        return {"data": response}
    except Exception as e:
        return {"error": f"Une erreur est survenue : {str(e)}"}

if __name__ == "__main__":
    app.run()
