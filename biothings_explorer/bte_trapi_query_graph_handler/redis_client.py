import redis
import os
from dotenv import load_dotenv

load_dotenv()

enable_redis = os.getenv('REDIS_HOST') and os.getenv('REDIS_POST')

if enable_redis:
    client = redis.Redis(port=os.getenv('REDIS_POST'), host=os.getenv('REDIS_HOST'))
else:
    client = None
