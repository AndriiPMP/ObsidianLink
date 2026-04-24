from pymongo.operations import SearchIndexModel
from configuration import (
    mongo_client,
    MONGODB_COLLECTION,
    MONGODB_VECTOR_INDEX,
    MONGODB_VECTOR_DIMENSIONS,
    MONGODB_DB
)


def create_collection_if_not_exists():

    db = mongo_client[MONGODB_DB]

    if MONGODB_COLLECTION not in db.list_collection_names():
        db.create_collection(MONGODB_COLLECTION)

    collection = db[MONGODB_COLLECTION]

    existing_indexes = {index["name"] for index in collection.list_search_indexes()}

    if MONGODB_VECTOR_INDEX not in existing_indexes:
        vector_index = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": MONGODB_VECTOR_DIMENSIONS,
                        "similarity": "cosine",
                    }
                ]
            },

            name = MONGODB_VECTOR_INDEX,
            type="vectorSearch",
        )

        collection.create_search_index(model=vector_index)

def add_document(client, collection_name, vector, formated_path, full_path, content):

    db = client[MONGODB_DB]

    collection = db[collection_name]

    collection.update_one(
        {"_id": formated_path},
        {
            "$set":{
                "formated_path": formated_path,
                "full_path": full_path,
                "content": content,
                "embedding": vector,
            }
        },
        
        upsert=True,
    )




