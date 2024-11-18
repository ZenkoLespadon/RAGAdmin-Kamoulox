import chromadb

from database_utils import creation_id


def create_collection_and_instanciate_collection(db, pdf_content):
    collection = db.create_collection("documentation")

    for i in pdf_content:
        for j in i:
            collection.add(
                document=j,
                ids=creation_id(j)
            )

    return  collection