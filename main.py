from configuration import client, r
from script.qdrant_integr import create_collection_if_not_exists
from script.qdrant_search import process_links
from redis_implement.redis_queue import init_queue
from script.get_vector import index_files
import time

collection_name = "obsidian_base"

def main():
    print("=== ObsidianLinks запущен ===\n")
    
    print("=== ЭТАП 1: Индексация файлов ===")
    
    print("1. Создаём коллекцию Qdrant...")
    create_collection_if_not_exists()
    
    print("2. Инициализируем очередь задач...")
    init_queue()
    
    print("3. Создаём embeddings и добавляем в Qdrant...")
    index_files()
    
    print("\n=== ЭТАП 2: Добавление ссылок ===")
    
    print("4. Пересоздаём очередь...")
    init_queue()
    
    print("5. Ищем похожие файлы и добавляем ссылки...")
    process_links()
    
    print("\n=== Готово! ===")


if __name__ == "__main__":
    main()


