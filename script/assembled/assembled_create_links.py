from script.mongo.mongo_integr import create_collection_if_not_exists
from script.mongo.mongo_search import process_links
from redis_implement.redis_queue import init_queue
from script.mongo.mongo_get_vector import index_files
from script.others.create_backUp import create_backup
from redis_implement.redis_queue_store import delete_store
from script.others.files_process import get_files_data
from configuration import MONGODB_COLLECTION

collection_name = MONGODB_COLLECTION

STAGE = 0

def create_links():
    global STAGE


    create_backup()

    if STAGE == 0:

        create_collection_if_not_exists()

        init_queue(get_files_data)

        index_files()

        STAGE = 1

    if STAGE == 1:

        init_queue(get_files_data)

        process_links()

        STAGE = 0

        delete_store()



