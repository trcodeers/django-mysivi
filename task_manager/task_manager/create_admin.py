from django.core.management.base import BaseCommand
from core.models import User, Company


class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **options):
        company, _ = Company.objects.get_or_create(name="Admin Company")

        if User.objects.filter(username="admin").exists():
            self.stdout.write("Admin already exists")
            return

        User.objects.create_superuser(
            username="admin",
            password="admin123",
            company=company
        )

        self.stdout.write("Admin user created")
