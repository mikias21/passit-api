from bson import ObjectId
from datetime import datetime
# Local import
from models.user_model import User, UserLogin
from models.user_account_verification_model import UserAccountVerificationModel

def create_new_user(user_email: str, 
                    user_password: str, 
                    user_ip: str,
                    user_browser: str,
                    user_browser_ver: str,
                    user_os: str,
                    user_os_ver: str,
                    user_device: str,
                    user_device_model: str,
                    otp: str,
                    user_lat,
                    user_long,
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
    new_user.user_signup_otp = otp
    new_user.user_signup_datetime = user_signup_datetime
    
    return dict(new_user)

def create_signin_user_record(user_email: str, 
                    user_ip: str,
                    user_browser: str,
                    user_browser_ver: str,
                    user_os: str,
                    user_os_ver: str,
                    user_device: str,
                    user_device_model: str,
                    user_lat: float,
                    user_long: float,
                    user_signin_datetime: str = str(datetime.now()), 
                    otp: str = ""):
    record = UserLogin()
    record.user_id = ObjectId()
    record.user_email = user_email
    record.user_signin_ip = user_ip
    record.user_signin_browser = user_browser
    record.user_signin_browser_version = user_browser_ver
    record.user_signin_os = user_os
    record.user_signin_os_version = user_os_ver
    record.user_signin_device = user_device
    record.user_signin_device_model = user_device_model
    record.user_signin_latitude = user_lat
    record.user_signin_longtiude = user_long
    record.user_signin_otp = otp
    record.user_signin_datetime = user_signin_datetime

    return dict(record)


def create_account_verification_record(email: str, verification_token: str, otp_code: str, user_ip: str,
                    user_browser: str,
                    user_browser_ver: str,
                    user_os: str,
                    user_os_ver: str,
                    user_device: str,
                    user_device_model: str,
                    user_lat: float,
                    user_long: float,
                    otp_identifier: str,
                    verify_datetime: str = str(datetime.now())):
    record = UserAccountVerificationModel()
    record.rec_id = ObjectId()
    record.user_email = email
    record.user_verification_token = verification_token
    record.otp_code = otp_code
    record.ip_address = user_ip
    record.user_browser = user_browser
    record.user_browser_version = user_browser_ver
    record.user_os = user_os
    record.user_os_version = user_os_ver
    record.user_device = user_device
    record.user_device_model = user_device_model
    record.user_latitude = user_lat
    record.user_longitude = user_long
    record.user_datetime = verify_datetime
    record.otp_identifier = otp_identifier

    return dict(record)