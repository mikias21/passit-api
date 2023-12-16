from bson import ObjectId
from schematics.models import Model
from schematics.types import StringType, EmailType, URLType, BaseType, DateTimeType

class UserPasswords(Model):
    password_id = BaseType(default=lambda: ObjectId(), serialize_when_none=False)
    label = StringType(required=True, max_length=20)
    password = StringType(required=True, max_length=50)
    category = StringType(max_length=20)
    url = URLType(verify_exists=True)
    description = StringType(max_length=200)
    owner_email = EmailType(required=True)
    added_date_time = DateTimeType(required=True)