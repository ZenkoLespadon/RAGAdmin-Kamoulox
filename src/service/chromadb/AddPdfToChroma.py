import os
from document_service import DocumentService
from vector_store_service import VectorStoreService
from langchain.schema import Document

def add_pdf_to_chroma(pdf_path: str):
    """
    Ajoute un document PDF dans la base de données ChromaDB avec suivi de l'état d'avancement.

    :param pdf_path: Chemin du fichier PDF à indexer.
    """
    try:
        print("📂 Vérification du fichier...")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"❌ Le fichier {pdf_path} n'existe pas.")

        # Initialiser les services
        print("⚙️ Initialisation des services...")
        doc_service = DocumentService()
        vector_store = VectorStoreService()

        # Extraction du texte du PDF
        print(f"📜 Extraction du texte depuis {pdf_path}...")
        with open(pdf_path, "rb") as pdf_file:
            pdf_text = doc_service.process_file(pdf_file, "pdf")

        print(f"✅ Extraction terminée ! Texte récupéré ({len(pdf_text)} caractères).")

        # Associer des métadonnées au document
        metadata = {"filename": os.path.basename(pdf_path), "source": pdf_path}

        # Découpage en chunks
        print("🔪 Découpage du texte en chunks...")
        documents = doc_service.store_document(pdf_text, metadata)
        print(f"✅ {len(documents)} chunks générés.")

        # Ajout dans ChromaDB
        print("📤 Ajout des documents dans ChromaDB...")
        vector_store.add_documents(documents)

        print(f"✅ {len(documents)} chunks du PDF '{pdf_path}' ajoutés avec succès à ChromaDB ! 🚀")

    except Exception as e:
        print(f"❌ Erreur lors de l'ajout du PDF à ChromaDB : {str(e)}")

add_pdf_to_chroma("Codedelaroute.pdf")
