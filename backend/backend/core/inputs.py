from graphene import ID, Int, String


class ForgotPasswordInput:
    email = String(required=True)


class ResetPasswordInput:
    key = String(required=True)
    password = String(required=True)
    confirm_password = String(required=True)


class RegisterInput:
    password = String(required=True)
    username = String(required=True)


class VerifyUserInput:
    user_id = ID(required=True)
    token = String(required=True)


class RequestOTPInput:
    phone = String(required=True)


class CreateUploadInput:
    kind = Int(required=True)
    name = String(required=True)
    mimetype = String(required=True)


class IDInput:
    id = ID(required=True)
