import redis
import os 
from pymongo import MongoClient


# Initialize Redis client
def get_redis_client():
    return redis.Redis(host=os.getenv("REDIS_HOST",'localhost'), port=6379, db=0)

# Dependency
def get_redis_dependency():
    redis_client = get_redis_client()
    try:
        yield redis_client
    finally:
        redis_client.close()
        pass

mongo_client = None

def init_mongo_client():
    global mongo_client
    mongo_client = MongoClient(
        os.getenv("MONGO_HOST", 'localhost'),
        int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER", 'admin'),
        password=os.getenv("MONGO_PASSWORD", 'admin')
    )

def close_mongo_client():
    global mongo_client
    mongo_client.close()

def get_mongo_client():
    global mongo_client
    return mongo_client

def get_mongo_dependency():
    client = get_mongo_client()
    try:
        yield client
    finally:
        # Don't close the client here.
        pass