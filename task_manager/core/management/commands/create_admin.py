from django.core.management.base import BaseCommand
from core.models import User, Company


class Command(BaseCommand):
    help = "Create admin user for ADMIN_COMPANY"

    def handle(self, *args, **options):
        company, _ = Company.objects.get_or_create(
            name="ADMIN_COMPANY"
        )

        if User.objects.filter(username="admin").exists():
            self.stdout.write("Admin already exists")
            return

        # This credentials should come from env variables or secure vault in real scenarios
        User.objects.create_superuser(
            username="admin",
            password="admin123",
            company=company
        )

        self.stdout.write("Admin user created successfully")
