from script.mongo_integr import create_collection_if_not_exists
from script.mongo_search import process_links
from redis_implement.redis_queue import init_queue
from script.get_vector import index_files
from script.create_backUp import create_backup
from configuration import MONGODB_COLLECTION

collection_name = MONGODB_COLLECTION

STAGE = 0

def main():
    global STAGE


    create_backup()

    if STAGE == 0:

        create_collection_if_not_exists()

        init_queue()

        index_files()

        STAGE = 1

    if STAGE == 1:

        init_queue()

        process_links()

        STAGE = 0
    


if __name__ == "__main__":
    main()


