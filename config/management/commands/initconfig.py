from django.core.management.base import BaseCommand
from config.enums import ConfigKeys, AppName
from config.models import *

class Command(BaseCommand):
    help = 'Initialise Configuration fields.'

    def handle(self, *args, **options):
        CONFIG_FIELDS = [
            {
                'config_key': ConfigKeys.COMPANY_NAME.value,
                'config_value': '',
                'app_name': AppName.GENERAL.value
            },
            {
                'config_key': ConfigKeys.VOUCHER_CODE_PREFIX.value,
                'config_value': '',
                'app_name': AppName.MARKETING.value
            },
            {
                'config_key': ConfigKeys.VOUCHER_LATEST_CODE.value,
                'config_value': 1,
                'app_name': AppName.MARKETING.value
            },
        ]
        try:
            if AppConfig.objects.exists():
                AppConfig.objects.all().delete()
            for field in CONFIG_FIELDS:
                AppConfig.objects.create(**field)
            self.stdout.write(self.style.SUCCESS('Configuration fields are successfully initialised with default values'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))