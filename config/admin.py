from django.contrib import admin
from config.models import AppConfig

# Register your models here.
@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ('config_key', 'app_name', 'config_value')
    search_fields = ('config_key', 'app_name')