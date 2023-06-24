from django.db.models import *
from django.apps import apps

# Create your models here.

class AppConfig(Model):
    APP_CHOICES = [(app.name, app.name) for app in apps.get_app_configs() if not app.name.startswith('django.') and not app.name.startswith('rest_') and not app.name.startswith('drf') and app.name not in ['storages']]+[('general', 'general')]

    config_id = BigAutoField(primary_key=True)
    app_name = CharField(max_length=255, unique=True, null=False, blank=False, choices=APP_CHOICES)
    config_key = CharField(max_length=255, null=False, blank=False)
    config_value = TextField(null=False, blank=False)

    class Meta:
        db_table = 'app_config'
        verbose_name_plural = 'App Configurations'
        unique_together = ('config_key',)