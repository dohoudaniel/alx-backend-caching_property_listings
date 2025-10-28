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
    Connect to Redis via django_redis and retrieve keyspace hits/misses from INFO.

    Returns:
        dict: {
            "keyspace_hits": int,
            "keyspace_misses": int,
            "hit_ratio": float or None,   # None if no ops yet
            "raw_info": dict,            # subset of returned INFO for debugging
        }
    Notes:
        - keyspace_hits/misses are server-wide metrics (not per-db).
        - If redis INFO does not include the fields, values default to 0.
    """
    try:
        # get_redis_connection will return a redis-py client (StrictRedis/Redis)
        conn = get_redis_connection("default")
        info = conn.info()  # returns a big dict of server stats
    except Exception as exc:
        logger.exception("Failed to connect to Redis to collect metrics: %s", exc)
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": None,
            "error": str(exc),
        }

    hits = int(info.get("keyspace_hits", 0))
    misses = int(info.get("keyspace_misses", 0))
    total = hits + misses

    hit_ratio = None
    if total > 0:
        hit_ratio = hits / total

    # Log the metrics at INFO level
    logger.info("Redis cache metrics — hits: %d, misses: %d, hit_ratio: %s", hits, misses, 
                f"{hit_ratio:.3f}" if hit_ratio is not None else "N/A")

    # Return a useful structure for programmatic inspection
    return {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
        "raw_info": {
            "used_memory_human": info.get("used_memory_human"),
            "instantaneous_ops_per_sec": info.get("instantaneous_ops_per_sec"),
            # include any other small diagnostics you find useful
        },
    }
