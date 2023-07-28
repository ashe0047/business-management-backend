from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='shapebeautyadmin').exists():
            User.objects.create_superuser(username='shapebeautyadmin', email='shapebeautysc@gmail.com', name='Shape Beauty Admin', password='9761988shape')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.ERROR('Superuser already exists.'))
