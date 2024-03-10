import redis

# Initialize Redis client
def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)

# Dependency
def get_redis_dependency():
    redis_client = get_redis_client()
    try:
        yield redis_client
    finally:
        redis_client.close()
        pass