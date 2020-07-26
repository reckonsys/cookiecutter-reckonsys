from hashlib import md5

from celery import current_app
from django.conf import settings
from django.core.mail import send_mail
from graphene import Boolean, Field
from graphene.relay import ClientIDMutation
from graphql import GraphQLError
from graphql_jwt.relay import JSONWebTokenMutation, Refresh, Revoke, Verify

from backend.core.choices import UploadStatus
from backend.core.decorators import login_required
from backend.core.inputs import (
    CreateUploadInput, ForgotPasswordInput, IDInput, RegisterInput,
    RequestOTPInput, ResetPasswordInput, VerifyUserInput)
from backend.core.models import Upload, User
from backend.core.node import Node
from backend.core.sms import send_sms
from backend.core.types import UploadType, UserType


def send_reset_email(user):
    _hash = md5(user.password.encode()).hexdigest()
    subject = "Reset You Password"
    # from_email = settings.EMAIL_HOST_USER
    from_email = 'no-reply@example.com'
    send_to = [user.email]
    message = f"Hi, To reset password click on this link: {settings.FRONTEND_PREFIX}/reset/{_hash}:{user.id}"  # noqa: E501
    send_mail(subject, message, from_email, send_to)


class Login(JSONWebTokenMutation):
    user = Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class ForgotPassword(ClientIDMutation):
    Input = ForgotPasswordInput
    user = Field(UserType)

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        try:
            user = User.objects.get(email=input.get('email'))
            send_reset_email(user)
        except User.DoesNotExist:
            raise GraphQLError('The email does not match any user')
        return ForgotPassword(user=user)


class ResetPassword(ClientIDMutation):
    Input = ResetPasswordInput
    user = Field(UserType)

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        password = input.get('password')
        try:
            _hash, user_id = input.get('key').split(":")
            user = User.objects.get(id=user_id)
            if _hash == md5(user.password.encode()).hexdigest():
                user.set_password(password)
                user.save()
            else:
                return GraphQLError('The key is tampered, please try again')
        except User.DoesNotExist:
            raise GraphQLError('The key does not match any user')
        if password != input.get('confirm_password'):
            raise GraphQLError('Password does not match')
        return ResetPassword(user=user)


class Register(ClientIDMutation):
    Input = RegisterInput
    user = Field(UserType)

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        password = input.get('password')
        username = input.get('username')
        try:
            user = User.objects.get(username=username)
            return GraphQLError('This credential is already used')
        except User.DoesNotExist:
            pass
        user = User.objects.create(username=username, email=username)
        user.set_password(password)
        # user.reset_password_key = ''
        user.save()
        # TODO: actually send email
        return Register(user=user)


class VerifyUser(ClientIDMutation):
    Input = VerifyUserInput
    user = Field(UserType)

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        user_id = input.get('user_id')
        token = input.get('token')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return GraphQLError('Unknown user')
        if user.validate_verify_token(token):
            user.is_verified = True
            user.save()
            return VerifyUser(user=user)
        else:
            return GraphQLError('This token is invalid')


class RequestOTP(ClientIDMutation):
    Input = RequestOTPInput
    success = Field(Boolean)

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        phone = input.get('phone')
        try:
            user = User.objects.get(phone=phone)
            user.reset_otp()
            send_sms(user.phone, f"Your login OTP is: {user.otp}")
            return RequestOTP(success=True)
        except User.DoesNotExist:
            return RequestOTP(success=False)


class CreateUpload(ClientIDMutation):
    Input = CreateUploadInput
    upload = Field(UploadType)

    @staticmethod
    @login_required
    def mutate_and_get_payload(root, info, **input):
        upload = Upload.objects.create(user=info.context.user, **input)
        return CreateUpload(upload=upload)


class UploadFinished(ClientIDMutation):
    Input = IDInput
    upload = Field(UploadType)

    @staticmethod
    @login_required
    def mutate_and_get_payload(root, info, **input):
        upload = Upload.objects.get(id=Node.gid2id(input.get('id')))
        upload.status = UploadStatus.UPLOADED
        upload.save()
        current_app.send_task(
            'backend.contrib.tasks.process_upload', (upload.id, ))
        return UploadFinished(upload=upload)


class CoreMutation:
    forgot_password = ForgotPassword.Field()
    login = Login.Field()
    refresh_token = Refresh.Field()
    register = Register.Field()
    request_otp = RequestOTP.Field()
    reset_password = ResetPassword.Field()
    revoke_token = Revoke.Field()
    verify_token = Verify.Field()
    verify_user = VerifyUser.Field()
    node = Node.Field()
    create_upload = CreateUpload.Field()
    upload_finished = UploadFinished.Field()
