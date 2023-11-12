from bson import ObjectId
from datetime import datetime
# Local import
from models.user_model import User

def create_new_user(user_email: str, 
                    user_password: str, 
                    user_ip: str,
                    user_browser: str,
                    user_browser_ver: str,
                    user_os: str,
                    user_os_ver: str,
                    user_device: str,
                    user_device_model: str,
                    user_lat: float,
                    user_long: float,
                    user_signup_datetime: str = str(datetime.now())):
    new_user = User()
    new_user.user_id = ObjectId()
    new_user.user_email = user_email
    new_user.user_password = user_password
    new_user.user_signup_ip = user_ip
    new_user.user_signup_browser = user_browser
    new_user.user_signup_browser_version = user_browser_ver
    new_user.user_signup_os = user_os
    new_user.user_signup_os_version = user_os_ver
    new_user.user_signup_device = user_device
    new_user.user_signup_device_model = user_device_model
    new_user.user_signup_latitude = user_lat
    new_user.user_signup_longtiude = user_long
    new_user.user_signup_datetime = user_signup_datetime
    
    return dict(new_user)