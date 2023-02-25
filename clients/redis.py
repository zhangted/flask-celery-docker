import os
import redis

def get_redis_connection():
  redis_url = os.getenv('REDIS_URL')
  redis_client = redis.from_url(redis_url)
  return redis_client