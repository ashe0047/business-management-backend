from django.core.cache import cache
from config.models import AppConfig
#config key,value retrieve function
CACHE_KEY = 'config_cache'
def get_config_value(key):
    #retrieve config cache from cache
    config_cache = cache.get(CACHE_KEY)
    #check for existence of cache, if None then load configs from db and store in cache
    if config_cache is None:
        config_cache = {config.config_key : config.config_value for config in AppConfig.objects.all()}
        cache.set(CACHE_KEY, config_cache)
    
    #check if config key/value exists 
    if not config_cache.get(key):
        raise KeyError('Config key '+key+' does not exists')
    
    return config_cache.get(key)