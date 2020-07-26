from django.core.management import call_command
from django.core.management.base import BaseCommand

from backend.core.choices import UserKind
from backend.core.models import User

MAIL = 'ad@ad.ad'

ADMINS = ['foo@example.com']


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('migrate', interactive=True)
        if not User.objects.filter(email=MAIL).exists():
            user = User.objects.create_superuser(email=MAIL, username=MAIL, kind=UserKind.ADMIN)  # noqa: E501
            user.set_password(MAIL)
            user.save()
        for email in ADMINS:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = email
                user.set_password('ad@ad.ad')
                user.save()
