# inventory/signals.py

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from inventory.models import MedicineDetail
from utils.redis_cache import RedisCache

cache_manager = RedisCache()
app_logger = logging.getLogger("app_logger")

# Define cache keys and lock templates
MEDICINE_LIST_CACHE_KEY = "medicine_list"
MEDICINE_DETAIL_CACHE_KEY_TEMPLATE = "medicine_detail_{}"
SEARCH_CACHE_KEY_TEMPLATE = "medicine_search_{}"
LOCK_KEY_TEMPLATE = "lock_key_{}"


def invalidate_cache_for_medicine(instance):
    # Attempt to acquire necessary locks
    list_lock = cache_manager.acquire_lock(MEDICINE_LIST_CACHE_KEY)
    detail_lock = cache_manager.acquire_lock(
        MEDICINE_DETAIL_CACHE_KEY_TEMPLATE.format(instance.id)
    )

    try:
        # Invalidate the main list cache
        cache_manager.delete(MEDICINE_LIST_CACHE_KEY)

        # Invalidate detail cache for the specific medicine instance
        cache_manager.delete(MEDICINE_DETAIL_CACHE_KEY_TEMPLATE.format(instance.id))

        # Invalidate search caches related to medicine's name and generic name
        query_terms = [instance.name, instance.generic_name.name]
        for term in query_terms:
            search_cache_key = SEARCH_CACHE_KEY_TEMPLATE.format(term)
            cache_manager.delete(search_cache_key)

        app_logger.info(
            "Cache invalidated for medicine ID %s and related keys.", instance.id
        )

    finally:
        # Only release locks if they were successfully acquired
        if list_lock:
            cache_manager.release_lock(list_lock)
        if detail_lock:
            cache_manager.release_lock(detail_lock)


@receiver(post_save, sender=MedicineDetail)
def invalidate_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate caches upon creating or updating a MedicineDetail entry.
    """
    invalidate_cache_for_medicine(instance)


@receiver(post_delete, sender=MedicineDetail)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate caches upon deleting a MedicineDetail entry.
    """
    invalidate_cache_for_medicine(instance)
