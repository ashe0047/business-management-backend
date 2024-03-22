from django.db.models import *
from django.apps import apps
from config.enums import AppName

# Create your models here.

class AppConfig(Model):
    APP_CHOICES = [(app_name.value, app_name.value) for app_name in AppName]

    config_id = BigAutoField(primary_key=True)
    app_name = CharField(max_length=255, null=False, blank=False, choices=APP_CHOICES)
    config_key = CharField(max_length=255, null=False, blank=False)
    config_value = TextField(null=False, blank=False)

    class Meta:
        db_table = 'app_config'
        verbose_name_plural = 'App Configurations'
        unique_together = (('config_key', 'app_name',),)