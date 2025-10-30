from django.core.cache import cache
from .models import Property

CACHE_KEY = "all_properties"
CACHE_TIMEOUT = 60 * 60 

def get_all_properties():
    """
    Return all properties, using low-level cache.
    Caches an *evaluated* list of property dicts (not a QuerySet object).
    """
    data = cache.get(CACHE_KEY)
    if data is not None:
        return data

    queryset = Property.objects.all().values(
        'property_id', 'title', 'description', 'price', 'location', 'created_at'
    )
    data = list(queryset)
    cache.set(CACHE_KEY, data, CACHE_TIMEOUT)
    return data
