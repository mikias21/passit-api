from enum import Enum

class General(Enum):
    RELEASE = True
    ALLOWED_TAGS = ['a', 'b', 'blockquote', 'br', 'em', 'i', 'li', 'ol', 'p', 'strong', 'ul']
    ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'blockquote': ['cite']}
    LOCAL_URL = "http://localhost:3000"
    REMOTE_URL = "https://passitt.netlify.app"
    DIGITAL_OCEN = True