# properties/utils.py
from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieve all properties, using Redis cache.
    Caches queryset data (as list of dicts) for 1 hour = 3600 seconds.
    """
    data = cache.get("all_properties")
    if data is None:
        # Fetch from DB and serialize as list of dicts
        queryset = Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        )
        data = list(queryset)
        cache.set("all_properties", data, 3600)  # store in Redis for 1 hour
    return data

