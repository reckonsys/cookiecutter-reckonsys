from boto3 import session as _session
from django.conf import settings

SENDER = {'DataType': 'String', 'StringValue': 'BACKEND'}
TYPE = {'DataType': 'String', 'StringValue': 'Transactional'}
session = _session.Session(region_name=settings.AWS_BUCKET_REGION)
sns = session.client(
    'sns',
    region_name='ap-south-1',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def send_sms(phone_number, message):
    if settings.AWS_ACCESS_KEY_ID == "minioadmin":
        return print(phone_number, message)
    return sns.publish(
        PhoneNumber=phone_number,
        Message=message,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': SENDER,
            'AWS.SNS.SMS.SMSType':  TYPE,
        })
