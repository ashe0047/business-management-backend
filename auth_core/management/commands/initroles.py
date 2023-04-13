from django.core.management.base import BaseCommand
from auth_core.management.commands.roles import init_roles_and_permissions

class Command(BaseCommand):
    help = 'Initializes roles and permissions.'
    
    def handle(self, *args, **options):
        init_roles_and_permissions()
