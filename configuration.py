from qdrant_client import QdrantClient 
import redis


client = QdrantClient(host="localhost", port=6333) # Подключаемся к квадранту


r = redis.Redis(host='localhost', port=6379, db=0)