from django.core.cache import cache
from .models import Property

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
