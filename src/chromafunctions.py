import chromadb
from chromadb.utils import embedding_functions
from pdf_to_txt import convert_pdf_en_txt

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
    convert_pdf_en_txt(documentpdf_path, doc_txt)
    add_documenttxt(doc_txt, collection_name)
        
        
    
def add_documenttxt(doc_txt, collection_name):
    try:
        client = get_client()
        collection = client.get_collection(collection_name)
        # Initialisation des listes pour le contenu des pages et les métadonnées des numéros de page
        documents = []
        metadatas = []
        
        # Lecture du fichier
        with open(doc_txt, 'r', encoding='utf-8') as file:
            page_content = []  # Contenu temporaire pour une page
            page_num = 2       # Initialisation du numéro de page
            
            for line in file:
                # Si la ligne contient une indication de page du type "p.<numéro>", cela signifie le début de la page suivante
                if f"=== Page {page_num} ===" in line:
                    # Ajout du contenu de la page dans le tableau documents et du numéro de page dans le tableau metadatas
                    clean_content = "".join(page_content).replace("\n", "").strip()
                    documents.append(clean_content)
                    metadatas.append(page_num-1)
                    
                    # Préparation pour la page suivante
                    page_content = []  # Réinitialisation du contenu de la page
                    page_num += 1      # Incrémentation du numéro de page
                else:
                    # Ajout de la ligne au contenu de la page actuelle
                    page_content.append(line)
            
            # Ajouter la dernière page si elle ne se termine pas par un numéro de page
            if page_content:
                clean_content = "".join(page_content).replace("\n", "").strip()
                documents.append(clean_content)
                metadatas.append(page_num-1)

        existing_ids = set(collection.get()['ids'])

        for i, (page_content, page_number) in enumerate(zip(documents, metadatas)):
            # Créer un identifiant unique qui n'est pas dans les IDs existants
            doc_id = f"doc_{i + 1}"
            counter=i
            while doc_id in existing_ids:
                counter=counter+1
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

def add_documents_from_folder_pdf(folder_path, collection_name):
    try:
        if not os.path.isdir(folder_path):
            raise ValueError(f"Le chemin fourni '{folder_path}' n'est pas un dossier valide.")
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path) and file_path.lower().endswith(".pdf"):
                print(f"Traitement du fichier PDF : {file_path}")
                ajout_documentpdf(file_path, collection_name)
            else:
                print(f"Le fichier {file_path} n'est pas un PDF ou n'a pas pu être ajouté à chromaDB")
    except Exception as e:
        print("Une erreur a eu lieu :", e)

def add_documents_from_folder_txt(folder_path, collection_name):
    try:
        if not os.path.isdir(folder_path):
            raise ValueError(f"Le chemin fourni '{folder_path}' n'est pas un dossier valide.")
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path) and file_path.lower().endswith(".txt"):
                print(f"Traitement du fichier TXT : {file_path}")
                ajout_documenttxt(file_path, collection_name)
            else:
                print(f"Le fichier {file_path} n'est pas un TXT ou n'a pas pu être ajouté à chromaDB")
    except Exception as e:
        print("Une erreur a eu lieu :", e)