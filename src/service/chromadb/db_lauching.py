from chromadb import Client

from conversion import pdf_to_text
from database import create_collection_and_instanciate_collection
from indexing import indexing_file, indexing_pdf_files
from reading_files import reading_files_pdf, getting_data_from_pdf
import os
#file that will be removed once the real config will be done for the server
# Définir la variable d'environnement pour ChromaDB
os.environ["CHROMA_DB_PATH"] = "/db"

dir_to_search = "/home/guillaume/Documents/dev/git/python/RAGAdmin/src/service/chromadb/doc"

if __name__ == "__main__":
    doc = []
    client = Client()

    list_files = indexing_file(dir_to_search)
    pdf_files = indexing_pdf_files(dir_to_search)
    pdf_content_read = getting_data_from_pdf(dir_to_search, pdf_files)
    doc = pdf_to_text(pdf_content_read)
    #relier le LLM à la variable collection le reste n'est pas important dans le contexte du LLM
    collection = create_collection_and_instanciate_collection(client, doc)
