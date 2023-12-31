from enum import Enum

class PasswordErrorMessages(Enum):
    PASSWORD_NOT_FOUND = "Password not found in our records."
    INVALID_LABEL = "Label should letters and numbers only and at most 20 characters."
    INVALID_CATEGORY = "Category should letters and numbers only and at most 20 characters."
    INVALID_URL = "Please use valid url for password."
    LABEL_USED = "Password with this label already exsit please use a unique label to avoid overwritting."
    NOT_FOUND = "Password not found with this id."
    CONFIRM_PASSWORD_LABEL = "Confirm again password label in the input box."
    URL_LENGTH_EXCEEDED = "URL length exceeded, try to use the domain name only."