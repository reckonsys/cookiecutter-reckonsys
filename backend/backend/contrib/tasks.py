from backend.core.choices import UploadKind, UploadStatus
from backend.core.tasks import task, logger
from backend.core.models import Upload


def _process_profile_picture(upload):
    pass


def _process_excel_report(upload):
    pass


_PROCESS_MAP = {
    UploadKind.PROFILE_PICTURE: _process_profile_picture,
    UploadKind.EXCEL_REPORT: _process_excel_report,
}


@task
def process_upload(upload_id):
    upload = Upload.objects.get(id=upload_id)
    try:
        _PROCESS_MAP[upload.kind](upload)
        upload.status = UploadStatus.PROCESSED
    except Exception as e:
        upload.status = UploadStatus.ERROR
        upload.message = str(e)
        logger.error('Upload Error', e, upload_id)
    upload.save()


@task
def connnect(sid, data):
    pass


@task
def my_event(sid, data):
    pass


@task
def disconnect(sid):
    pass
