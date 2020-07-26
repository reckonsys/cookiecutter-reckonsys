import hmac
import random
from string import ascii_lowercase, digits
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE, CharField, DateTimeField, ForeignKey, Model,
    PositiveSmallIntegerField, TextField, UUIDField)

from backend.core.choices import UploadKind, UploadStatus, UserKind

ALPHANUM = ascii_lowercase + digits
OTP_LEN = 6


def get_otp():
    return ''.join(random.sample(ALPHANUM, OTP_LEN))


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True, editable=False)
    id = UUIDField(default=uuid4, primary_key=True, editable=False)
    updated_at = DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    kind = PositiveSmallIntegerField(choices=UserKind.CHOICES, default=UserKind.CLIENT)  # noqa: E501
    otp = CharField(max_length=OTP_LEN, null=True, blank=True)
    phone = CharField(max_length=15, null=True, blank=True)

    def get_verification_link(self):
        return f'{settings.FRONTEND_PREFIX}/verify/{self.id}/{self.get_verify_token()}'  # noqa: E501

    def get_verify_token(self):
        result = hmac.new(settings.SECRET_KEY.encode('utf-8'), msg=str(self.id).encode('utf-8'))  # noqa: E501
        return result.hexdigest()

    def validate_verify_token(self, digest):
        return hmac.compare_digest(digest, self.get_verify_token())

    def reset_otp(self):
        self.otp = get_otp()
        self.save()


class Upload(BaseModel):
    kind = PositiveSmallIntegerField(choices=UploadKind.CHOICES, default=UploadKind.PROFILE_PICTURE)  # noqa: E501
    message = TextField(null=True, blank=True)  # error messages, if any
    mimetype = CharField(max_length=100)
    name = CharField(max_length=250)  # original file name
    status = PositiveSmallIntegerField(choices=UploadStatus.CHOICES, default=UploadStatus.UPLOADING)  # noqa: E501
    user = ForeignKey(User, on_delete=CASCADE, related_name='uploads')

    @property
    def key(self):
        return f'uploads/{self.kind}/{self.id}'
