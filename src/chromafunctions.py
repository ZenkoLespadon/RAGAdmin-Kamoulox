import chromadb
from chromadb.utils import embedding_functions
from pdf_to_txt import convert_pdf_to_txt
from pdf_to_json import convert_pdf_to_json
from txt_to_json import convert_txt_to_json
import json
# Initialisation du client ChromaDB
client = None  # Initialisé à None
def get_client():
    global client
    if client is None:
        client = chromadb.HttpClient(host='192.168.0.22', port=8000)
    return client

def create_collection(collection_name: str):
    """
    Crée une nouvelle collection dans la base de données.
    """
    try:
        client = get_client()
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-mpnet-base-v2')
        collection = client.create_collection(collection_name)
        print(f"Collection '{collection_name}' créée avec succès.")
        return collection
    except Exception as e:
        print(f"Erreur lors de la création de la collection: {e}")
        return None

def delete_collection(collection_name: str):
    """
    Supprime une collection existante.
    """
    try:
        client = get_client()
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' supprimée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection: {e}")


def search_in_collection_text(collection_name: str, query_text: str, k=1):
    """
    Recherche dans la collection en fonction du contenu.
    """
    try:
        client = get_client()
        collection = client.get_collection(collection_name)
        results = collection.query(
            query_texts=query_text,
            n_results=k,  # Nombre de résultats à retourner
            include=['documents','metadatas']  # Inclure les documents dans les résultats
        )
        print(f"Résultats de la recherche :")
        print(f"{results}")
        return results
    except Exception as e:
        print(f"Erreur lors de la recherche dans la collection: {e}")
        return None

def search_in_collection_embedding(collection_name: str, query_embedding, k=1):
    """
    Recherche dans la collection en fonction des embeddings.
    """
    try:
        client = get_client()
        collection = client.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],  # Embedding de la requête
            n_results=k,  # Nombre de résultats à retourner
            include=['documents']  # Inclure les documents dans les résultats
        )
        print(f"Résultats de la recherche :")
        print(f"{results}")
        return results
    except Exception as e:
        print(f"Erreur lors de la recherche dans la collection: {e}")
        return None

def add_documentpdf(documentpdf_path, collection_name):
    doc_json = "document.json"
    convert_pdf_to_json(documentpdf_path, doc_json)
    add_documentjson(doc_json, collection_name)
        
        
    
def add_documenttxt(doc_txt, collection_name):
    doc_json = "document.json"
    convert_txt_to_json(doc_txt, doc_json)
    add_documentjson(doc_json, collection_name)


def add_documentjson(json_path, collection_name):
    try:
        client = get_client()
        collection = client.get_collection(collection_name)

        # Charger les données du fichier JSON
        with open(json_path, 'r', encoding='utf-8') as json_file:
            pages = json.load(json_file)

        existing_ids = set(collection.get()['ids'])

        for i, page in enumerate(pages):
            page_content = page["content"]
            page_number = page["page_number"]

            # Créer un identifiant unique qui n'est pas dans les IDs existants
            doc_id = f"doc_{i + 1}"
            counter = i
            while doc_id in existing_ids:
                counter += 1
                doc_id = f"doc_{counter + 1}"
            
            # Ajouter le nouvel ID à la liste des IDs existants pour éviter les conflits
            existing_ids.add(doc_id)
            
            # Ajouter le document avec son contenu et ses métadonnées
            collection.add(
                ids=[doc_id],
                documents=[page_content],
                metadatas=[{"page_number": page_number}]
            )
    except Exception as e:
        print("Une erreur a eu lieu :", e)