from graphene_django import DjangoObjectType

from backend.core.node import Node
from backend.core.models import User, Upload
from graphene.types import JSONString
from graphene_django import DjangoObjectType

from backend.core.storage import generate_presigned_post



class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node, )
        convert_choices_to_enum = False



class UploadType(DjangoObjectType):

    presigned_post_url = JSONString()

    class Meta:
        model = Upload
        interfaces = (Node, )
        convert_choices_to_enum = False

    def resolve_presigned_post_url(self, info):
        return generate_presigned_post(self.key)
