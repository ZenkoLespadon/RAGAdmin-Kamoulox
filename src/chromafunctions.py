import chromadb
from chromadb.utils import embedding_functions
from pdf_to_txt import convert_pdf_to_txt
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
    doc_txt = "document.txt"
    convert_pdf_to_txt(documentpdf_path, doc_txt)
    add_document_txt(doc_txt, collection_name)


def add_document_txt(txt_path, collection_name):
    """
    Ajoute un document TXT à une collection. Le contenu entier du fichier est considéré comme un document unique.
    """
    try:
        client = get_client()
        collection = client.get_collection(collection_name)

        # Charger le contenu du fichier TXT
        with open(txt_path, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read()

        # Vérifier les IDs existants dans la collection
        existing_ids = set(collection.get()['ids'])

        # Générer un identifiant unique pour le document
        doc_id = "doc_1"
        counter = 0
        while doc_id in existing_ids:
            counter += 1
            doc_id = f"doc_{counter}"
        
        # Ajouter le nouvel ID à la liste des IDs existants
        existing_ids.add(doc_id)
        
        # Ajouter le document avec son contenu
        collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[{"source": txt_path}]
        )
        print(f"Document '{txt_path}' ajouté avec succès avec l'ID '{doc_id}'.")
    except Exception as e:
        print("Une erreur a eu lieu :", e)
