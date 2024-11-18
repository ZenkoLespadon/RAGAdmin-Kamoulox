import chromadb

def create_collection_and_instanciate_collection(db):
    collection = db.create_collection("documentation")