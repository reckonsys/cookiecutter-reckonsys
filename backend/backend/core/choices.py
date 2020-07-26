from orm_choices import choices


@choices
class UserKind:
    class Meta:
        ADMIN = (1, 'Admin')
        CLIENT = (2, 'Client')


@choices
class UploadKind:
    class Meta:
        PROFILE_PICTURE = (1, 'Profile Picture')
        EXCEL_REPORT = (2, 'Excel Report')


@choices
class UploadStatus:
    class Meta:
        UPLOADING = (1, 'Uploading')
        UPLOADED = (2, 'Uploaded')
        PROCESSING = (3, 'Processing')
        PROCESSED = (4, 'Processed')
        ERROR = (5, 'Error')
