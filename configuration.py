import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import redis


MONGODB_URI = os.getenv("MONGODB_URI")
ONGODB_DB = os.getenv("MONGODB_DB", "obsidian")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "obsidian_base")
MONGODB_VECTOR_INDEX = os.getenv("MONGODB_VECTOR_INDEX", "obsidian_vector_index")
MONGODB_VECTOR_DIMENSIONS = int(os.getenv("MONGODB_VECTOR_DIMENSIONS", "4096"))

mongo_client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))

r = redis.Redis(host='localhost', port=6379, db=0)