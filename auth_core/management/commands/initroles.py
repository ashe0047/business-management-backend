from django.core.management.base import BaseCommand
from auth_core.models import Group
from auth_core.management.commands.roles import Roles
class Command(BaseCommand):
    help = 'Initializes roles and permissions.'
    
    def handle(self, *args, **options):
        try:
            for role in list(Roles):
                if not Group.objects.filter(name=role.value).exists():
                    Group.objects.create(name=role.value)
                self.stdout(self.style.WARNING(role.value+' already exists'))
        except Exception as e:
            self.stdout(self.style.ERROR(str(e)))
