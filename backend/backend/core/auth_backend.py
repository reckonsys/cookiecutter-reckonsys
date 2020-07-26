from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class PhoneOTPBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if username in [None, ''] or password in [None, '']:
            return None
        User = get_user_model()
        password = password.lower()
        qs = User.objects.filter(phone=username, otp=password)
        if not qs.exists():
            return None
        user = qs.get()
        user.otp = None
        user.save()
        return user
