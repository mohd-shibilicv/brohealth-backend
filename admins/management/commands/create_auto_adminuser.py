import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Admin's username")
        parser.add_argument("--email", help="Admin's email")
        parser.add_argument("--password", help="Admin's password")
        parser.add_argument(
            "--no-input", help="Read options from the environment", action="store_true"
        )

    def handle(self, *args, **options):
        User = get_user_model()

        if options["no_input"]:
            options["username"] = os.environ["DJANGO_SUPERUSER_USERNAME"]
            options["email"] = os.environ["DJANGO_SUPERUSER_EMAIL"]
            options["password"] = os.environ["DJANGO_SUPERUSER_PASSWORD"]

        if not User.objects.filter(email=options["email"]).exists():
            User.objects.create_superuser(
                first_name=options["username"],
                email=options["email"],
                password=options["password"],
            )
        else:
            raise CommandError('Admin user already exists')

        self.stdout.write(
                self.style.SUCCESS('Successfully created the admin user')
            )
