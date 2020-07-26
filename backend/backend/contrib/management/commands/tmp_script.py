from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Temp Command."

    def handle(self, *args, **options):
        print("Just a temp command to test a script quickly")
