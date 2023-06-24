from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'

    def ready(self) -> None:
        import config.signals
        from django.core.cache import cache
        from config.utils import CACHE_KEY
        from config.models import AppConfig
        # Fetch config values from the database and store in the cache if cache doesnt exists
        if not cache.get(CACHE_KEY):
            config_cache = {config.config_key: config.config_value for config in AppConfig.objects.all()}
            cache.set(CACHE_KEY, config_cache)
