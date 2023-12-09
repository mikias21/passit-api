from bson import ObjectId
from schematics.models import Model
from schematics.types import EmailType, StringType, FloatType, DateTimeType, BaseType, BooleanType

class UserAccountVerificationModel(Model):
    rec_id = BaseType(default=lambda: ObjectId(), serialize_when_none=False)
    user_email = EmailType(required=True)
    user_verification_token = StringType(required=True)
    otp_code = StringType(required=True)
    ip_address = StringType(required=True)
    user_browser = StringType(required=True)
    user_browser_version = StringType(required=True)
    user_os = StringType(required=True)
    user_os_version = StringType(required=True)
    user_device = StringType(required=True)
    user_device_model = StringType(required=True)
    user_latitude = FloatType(required=True)
    user_longitude = FloatType(required=True)
    otp_identifier = StringType(required=True)
    user_datetime = DateTimeType(required=True)