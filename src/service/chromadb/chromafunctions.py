import chromadb
from chromadb.utils import embedding_functions


def get_client(ip_host:str = "127.0.0.1"):
    try:
        client = chromadb.HttpClient(host=ip_host, port=8000)
    except Exception:
        client = None
    return client

def create_collection(collection_name: str,ip_host:str = "127.0.0.1"):
    """
    Crée une nouvelle collection dans la base de données.
    """
    try:
        client = get_client(ip_host)
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-mpnet-base-v2')
        collection = client.create_collection(collection_name)
        print(f"Collection '{collection_name}' créée avec succès.")
        return collection
    except Exception as e:
        print(f"Erreur lors de la création de la collection: {e}")
        return None

def delete_collection(collection_name: str,ip_host:str = "127.0.0.1"):
    """
    Supprime une collection existante.
    """
    try:
        client = get_client(ip_host)
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' supprimée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection: {e}")


def search_in_collection_text(collection_name: str, query_text: str, k:int=1,ip_host:str = "127.0.0.1"):
    """
    Recherche dans la collection en fonction du contenu.
    """
    try:
        client = get_client(ip_host)
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

def search_in_collection_embedding(collection_name: str, query_embedding, k:int=1,ip_host:str = "127.0.0.1"):
    """
    Recherche dans la collection en fonction des embeddings.
    """
    try:
        client = get_client(ip_host)
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



def add_document_txt(txt_path, collection_name,ip_host:str = "127.0.0.1"):
    """
    Ajoute un document TXT à une collection. Le contenu est divisé en morceaux (chunks)
    qui se superposent à 10 %, et chaque chunk est ajouté comme un document distinct.
    """
    try:
        client = get_client(ip_host)
        collection = client.get_collection(collection_name)

        # Charger le contenu du fichier TXT
        with open(txt_path, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read()

        # Fonction pour diviser le texte en chunks avec chevauchement
        def split_into_chunks(text, chunk_size, overlap):
            step = chunk_size - overlap
            chunks = [
                text[i:i + chunk_size]
                for i in range(0, len(text), step)
                if i + chunk_size <= len(text) or len(text) - i > overlap
            ]
            return chunks

        # Définir la taille des chunks et le chevauchement (en caractères)
        chunk_size = 1000  # Taille de chaque chunk (par exemple 1000 caractères)
        overlap = int(chunk_size * 0.1)  # 10 % de chevauchement

        # Diviser le contenu en chunks
        chunks = split_into_chunks(content, chunk_size, overlap)

        # Vérifier les IDs existants dans la collection
        existing_ids = set(collection.get()['ids'])

        # Ajouter chaque chunk comme un document avec un ID unique
        for index, chunk in enumerate(chunks):
            doc_id = f"doc_{index}"
            counter = 0
            while doc_id in existing_ids:
                counter += 1
                doc_id = f"doc_{counter}"

            # Ajouter le document avec son contenu
            collection.add(
                ids=[doc_id],
                documents=[chunk],
                metadatas=[{"source": txt_path, "chunk_index": index}]
            )

        print(f"Document '{txt_path}' divisé en {len(chunks)} chunks et ajouté avec succès à la collection '{collection_name}'.")

    except Exception as e:
        print("Une erreur a eu lieu :", e)

def delete_a_file_in_the_collection(txt_path:str, collection_name:str,ip_host:str = "127.0.0.1"):
    client = get_client(ip_host)
    collection = client.get_collection(collection_name)

    results = collection.query(where={"source": txt_path})
    ids_to_delete = [result["id"] for result in results["documents"]]
    collection.delete(ids=ids_to_delete)

if __name__ == "__main__":
    Collection_name = "docs"
