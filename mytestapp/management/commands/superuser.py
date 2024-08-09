from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username=settings.SUPERUSER_NAME).exists():
            User.objects.create_superuser(
                username=settings.SUPERUSER_NAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser {settings.SUPERUSER_NAME} created successfully'))