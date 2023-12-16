from enum import Enum

class PasswordErrorMessages(Enum):
    PASSWORD_NOT_FOUND = "Password not found in our records."
    INVALID_LABEL = "Label should letters and numbers only and at most 20 characters."
    INVALID_CATEGORY = "Category should letters and numbers only and at most 20 characters."
    INVALID_URL = "Please use valid url for password."
    LABEL_USED = "Password with this label already exsit please use a unique label to avoid overwritting."
    NOT_FOUND = "Password not found with this id."