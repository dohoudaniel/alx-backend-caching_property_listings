# properties/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Property)
def clear_all_properties_cache_on_save(sender, instance, created, **kwargs):
    """
    Clear the cached 'all_properties' when a Property is created or updated.
    """
    cache.delete("all_properties")
    logger.info("Cleared cache key 'all_properties' due to save on Property id=%s (created=%s)", getattr(instance, "id", None), created)

@receiver(post_delete, sender=Property)
def clear_all_properties_cache_on_delete(sender, instance, **kwargs):
    """
    Clear the cached 'all_properties' when a Property is deleted.
    """
    cache.delete("all_properties")
    logger.info("Cleared cache key 'all_properties' due to delete on Property id=%s", getattr(instance, "id", None))

