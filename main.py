from script.mongo_integr import create_collection_if_not_exists
from script.mongo_search import process_links
from redis_implement.redis_queue import init_queue
from script.get_vector import index_files
from configuration import MONGODB_COLLECTION

collection_name = MONGODB_COLLECTION

STAGE = 0

def main():
    global STAGE

    print("=== ObsidianLinks запущен ===\n")

    if STAGE == 0:
    
        print("=== ЭТАП 1: Индексация файлов ===")
    
        print("1. Создаём коллекцию MongoDB...")
        create_collection_if_not_exists()
    
        print("2. Инициализируем очередь задач...")
        init_queue()
    
        print("3. Создаём embeddings и добавляем в MongoDB...")
        index_files()

        STAGE = 1

    if STAGE == 1:
        print("\n=== ЭТАП 2: Добавление ссылок ===")
    
        print("4. Пересоздаём очередь...")
        init_queue()
    
        print("5. Ищем похожие файлы и добавляем ссылки...")
        process_links()

        STAGE = 0
    
    print("\n=== Готово! ===")


if __name__ == "__main__":
    main()


