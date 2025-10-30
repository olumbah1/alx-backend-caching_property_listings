import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Fetch all properties from cache if available,
    otherwise from database and store in cache for 1 hour (3600 seconds).
    """
    data = cache.get('all_properties')
    if data is not None:
        return data

    queryset = Property.objects.all().values(
        'property_id', 'title', 'description', 'price', 'location', 'created_at'
    )
    data = list(queryset)
    cache.set('all_properties', data, 3600)  
    return data


def get_redis_cache_metrics():
    """
    Connect to Redis via django_redis and return cache hit/miss metrics.

    Returns a dict:
        {
            'keyspace_hits': int,
            'keyspace_misses': int,
            'hit_ratio': float  # value between 0.0 and 1.0, or None if no requests yet
        }

    Also logs the metrics at INFO level.
    """
    try:
        # Use the default cache connection configured with django-redis
        client = get_redis_connection("default")

        # client.info() returns a dict with stats including 'keyspace_hits' and 'keyspace_misses'
        info = client.info()
        hits = int(info.get('keyspace_hits', 0))
        misses = int(info.get('keyspace_misses', 0))

        total = hits + misses
        if total > 0:
            hit_ratio = hits / total
        else:
            hit_ratio = None  # no requests yet

        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'hit_ratio': hit_ratio,
        }

        logger.info("Redis cache metrics: hits=%s misses=%s hit_ratio=%s", hits, misses, hit_ratio)
        return metrics

    except Exception as e:
        # Log exception and return a sensible default
        logger.exception("Failed to fetch Redis metrics: %s", e)
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': None,
            'error': str(e),
        }
