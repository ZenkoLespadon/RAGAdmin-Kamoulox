import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from vector_store_service import *
# Définir le chemin du stockage de ChromaDB
persist_dir = "./datas"

# Vérifier si la base ChromaDB existe
if not os.path.exists(persist_dir):
    print(f"❌ Le dossier {persist_dir} n'existe pas. Aucune base de données ChromaDB trouvée.")

# Définir le chemin du modèle et charger l'embedding function
vector_store_service = VectorStoreService()

# Afficher le nombre de documents dans la base
print("Nombre de documents :", vector_store_service.get_document_count())

search = "Que faire à un feu rouge ?"
print("Recherche = ",search)
print(vector_store_service.search_documents(search))
