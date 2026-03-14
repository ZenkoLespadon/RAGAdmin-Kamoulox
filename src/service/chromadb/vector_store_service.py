import logging
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

logger = logging.getLogger(__name__)

class VectorStoreService:

    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(model_name="./paraphrase-mpnet-base-v2")

        # Initialize vector store with existing database if it exists
        persist_dir = "./src/service/chromadb/datas"
        self.vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings,
            collection_name="documents"
        )

        collection_size = len(self.vector_store.get()['ids'])
        logger.info(f"Initialized Chroma database with {collection_size} existing documents")

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        try:
            # Add documents
            self.vector_store.add_documents(documents)
            self.vector_store.persist()

            # Verify size after addition
            collection_size = len(self.vector_store.get()['ids'])
            logger.info(f"Vector store now contains {collection_size} documents")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def search_documents(self, query: str, k: int = 10, threshold: float = 0.5) -> List[Document]:
        """Search for relevant documents based on query with improved reliability."""
        try:
            collection_size = self.get_document_count()
            if collection_size == 0:
                logger.warning("Vector store is empty!")
                return []

            logger.info(f"Searching in {collection_size} documents")

            # Perform similarity search with scores
            results_with_scores = self.vector_store.similarity_search_with_score(query, k=k * 2, filter=None)

            # Filter results based on similarity score threshold
            filtered_results = [
                doc for doc, score in results_with_scores if score >= threshold
            ]

            # Keep only the top-k most relevant documents
            filtered_results = filtered_results[:k]

            logger.info(f"Found {len(filtered_results)} relevant documents after filtering by threshold ({threshold})")

            return filtered_results

        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

    def delete_document(self, chroma_id: str) -> None:
        """Delete all chunks of a document from the vector store."""
        try:
            # Get all documents
            results = self.vector_store.get()

            # Find all chunks with matching chroma_id
            ids_to_delete = []
            for i, metadata in enumerate(results['metadatas']):
                if metadata.get('chroma_id') == chroma_id:
                    ids_to_delete.append(results['ids'][i])

            if ids_to_delete:
                # Delete all chunks
                self.vector_store._collection.delete(
                    ids=ids_to_delete
                )
                logger.info(f"Deleted {len(ids_to_delete)} chunks for document with chroma_id {chroma_id}")
            else:
                logger.warning(f"No chunks found for document with chroma_id {chroma_id}")

        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise

    def get_document_count(self) -> int:
        """Returns the number of documents in the Chroma database."""
        try:
            return len(self.vector_store.get()['ids'])
        except Exception as e:
            logger.error(f"Error retrieving document count: {str(e)}")
            return 0

	

