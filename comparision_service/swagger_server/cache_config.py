from flask_caching import Cache
import os


CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://redis_service:6379/0')
CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 10))

cache = Cache(config={
    'CACHE_TYPE': CACHE_TYPE,
    'CACHE_REDIS_URL': CACHE_REDIS_URL,
    'CACHE_DEFAULT_TIMEOUT': CACHE_DEFAULT_TIMEOUT
})
