# properties/utils.py
from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

# def get_all_properties():
#     """
#     Retrieve all properties, using Redis cache.
#     Caches queryset data (as list of dicts) for 1 hour = 3600 seconds.
#     """
#     data = cache.get("all_properties")
#     if data is None:
#     # Fetch from DB and serialize as list of dicts
    #     queryset = Property.objects.all().values(
    #     "id", "title", "description", "price", "location", "created_at"
#     )
#     data = list(queryset)
#     cache.set("all_properties", data, 3600)  # store in Redis for 1 hour
#     return data

def get_all_properties():
    """
    Retrieve all properties, using Redis cache.
    Caches serialized queryset data (as list of dicts) for 1 hour = 3600 seconds.
    """
    data = cache.get("all_properties")
    if data is None:
        queryset = Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        )
        data = list(queryset)
        cache.set("all_properties", data, 3600)
        logger.info("Cached 'all_properties' with %d items", len(data))
    else:
        logger.debug("Cache hit for 'all_properties' (items=%d)", len(data))
    return data


def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics and compute hit ratio.
    Logs key metrics and errors.
    """
    from django_redis import get_redis_connection

    try:
        conn = get_redis_connection("default")
        info = conn.info()
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0,
            "error": str(e),
        }

    keyspace_hits = int(info.get("keyspace_hits", 0))
    keyspace_misses = int(info.get("keyspace_misses", 0))
    total_requests = keyspace_hits + keyspace_misses

    hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0

    logger.info(
        f"Redis Metrics — Hits: {keyspace_hits}, Misses: {keyspace_misses}, "
        f"Hit Ratio: {hit_ratio:.2f}"
    )

    return {
        "keyspace_hits": keyspace_hits,
        "keyspace_misses": keyspace_misses,
        "hit_ratio": hit_ratio,
    }

