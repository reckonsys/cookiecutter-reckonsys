from graphene import ID, Field, List

from backend.core.decorators import login_required
from backend.core.models import Upload
from backend.core.node import Node
from backend.core.types import UploadType


class CoreQuery(object):
    uploads = Field(List(UploadType))
    upload = Field(UploadType, id=ID(required=True))

    @login_required
    def resolve_upload(self, info, id):
        return Upload.objects.get(id=Node.gid2id(id))

    @login_required
    def resolve_uploads(self, info):
        return Upload.objects.filter(user=info.context.user).order_by('-created_at')  # noqa: E501
