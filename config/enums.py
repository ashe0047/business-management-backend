from enum import Enum
from django.apps import apps

ConfigKeys = Enum('ConfigKeys', [(key, key) for key in ['COMPANY_NAME', 'VOUCHER_CODE_PREFIX', 'VOUCHER_LATEST_CODE']])

AppName = Enum('AppName', [(app.name.upper(), app.name) for app in apps.get_app_configs() if not app.name.startswith('django.') and not app.name.startswith('rest_') and not app.name.startswith('drf') and app.name not in ['storages']]+[('GENERAL', 'general')])

