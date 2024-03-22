from django.apps import AppConfig


class MarketingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketing'

    def ready(self) -> None:
        import marketing.signals
        return super().ready()
