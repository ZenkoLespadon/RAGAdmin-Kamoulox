import chromadb
from chromadb.utils import embedding_functions
from pdf_to_txt import convertir_pdf_en_txt

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

def add_documents_to_collection(collection_name: str, documents: list, metadatas: list):
    """
    Ajoute des documents dans la collection avec un ID unique pour chaque document.
    """
    try:
        client = get_client()
        collection = client.get_collection(collection_name)
        # Générer un ID unique pour chaque document
        ids = [f"id_{i+1}" for i in range(len(documents))]
        
        collection.add(
            documents=documents,    # Liste des documents à ajouter
            metadatas=metadatas,    # Liste des métadonnées correspondantes
            ids=ids                 # Liste d'IDs uniques générés
        )
        
        print(f"{len(documents)} documents ajoutés à la collection '{collection_name}'.")
    except Exception as e:
        print(f"Erreur lors de l'ajout des documents: {e}")

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

def ajout_documentpdf(document_path, collection_name):
    pdf_chemin = document_path  # Remplacez par votre fichier PDF
    txt_chemin = "data\\document.txt"  # Chemin de sortie pour le fichier TXT

    # Appeler la fonction
    convertir_pdf_en_txt(pdf_chemin, txt_chemin)
    
    client = get_client()
    collection = client.get_collection(collection_name)
    # Initialisation des listes pour le contenu des pages et les métadonnées des numéros de page
    documents = []
    metadonnees = []
    
    # Lecture du fichier
    with open(txt_chemin, 'r', encoding='utf-8') as file:
        page_contenu = []  # Contenu temporaire pour une page
        page_num = 2       # Initialisation du numéro de page
        
        for line in file:
            # Si la ligne contient une indication de page du type "p.<numéro>", cela signifie le début de la page suivante
            if f"=== Page {page_num} ===" in line:
                # Ajout du contenu de la page dans le tableau documents et du numéro de page dans le tableau metadonnees
                clean_content = "".join(page_contenu).replace("\n", "").strip()
                documents.append(clean_content)
                metadonnees.append(page_num-1)
                
                # Préparation pour la page suivante
                page_contenu = []  # Réinitialisation du contenu de la page
                page_num += 1      # Incrémentation du numéro de page
            else:
                # Ajout de la ligne au contenu de la page actuelle
                page_contenu.append(line)
        
        # Ajouter la dernière page si elle ne se termine pas par un numéro de page
        if page_contenu:
            clean_content = "".join(page_contenu).replace("\n", "").strip()
            documents.append(clean_content)
            metadonnees.append(page_num-1)

    for i, (page_content, page_number) in enumerate(zip(documents, metadonnees)):
        # Créer un identifiant unique pour chaque document (par exemple, "doc1", "doc2", ...)
        doc_id = f"doc_{i + 1}"
        
        # Ajouter le document avec son contenu et ses métadonnées
        collection.add(
            ids=doc_id,
            documents=page_content,
            metadatas={"page_number": page_number}
        )