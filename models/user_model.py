from bson import ObjectId
from schematics.models import Model
from schematics.types import EmailType, StringType, FloatType, DateTimeType, BaseType, BooleanType

class User(Model):
    user_id = BaseType(default=lambda: ObjectId(), serialize_when_none=False)
    user_email = EmailType(required=True)
    user_password = StringType(min_length=8, max_length=16, required=True)
    user_activated = BooleanType(default=False)
    user_signup_ip = StringType(required=True)
    user_signup_browser = StringType(required=True)
    user_signup_browser_version = StringType(required=True)
    user_signup_os = StringType(required=True)
    user_signup_os_version = StringType(required=True)
    user_signup_device = StringType(required=True)
    user_signup_device_model = StringType(required=True)
    user_signup_latitude = FloatType(required=True)
    user_signup_longitude = FloatType(required=True)
    user_signup_otp = StringType(required=True)
    user_signup_datetime = DateTimeType(required=True)