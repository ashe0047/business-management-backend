from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from config.models import AppConfig
from config.utils import CACHE_KEY

@receiver([post_save, post_delete], sender=AppConfig)
def update_config_cache(sender, instance, **kwargs):
    config_cache = cache.get(CACHE_KEY)
    if config_cache is not None:
        # Update the cache when a config value is added, updated, or deleted
        if kwargs.get('created', False):
            config_cache[instance.config_key] = instance.config_value
        else:
            config_cache.pop(instance.config_key, None)
        cache.set(CACHE_KEY, config_cache)