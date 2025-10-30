from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

CACHE_KEY = "all_properties"

@receiver(post_save, sender=Property)
def invalidate_all_properties_on_save(sender, instance, **kwargs):
    """
    Invalidate the cached 'all_properties' when a Property is created or updated.
    """
    cache.delete(CACHE_KEY)

@receiver(post_delete, sender=Property)
def invalidate_all_properties_on_delete(sender, instance, **kwargs):
    """
    Invalidate the cached 'all_properties' when a Property is deleted.
    """
    cache.delete(CACHE_KEY)
