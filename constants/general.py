from enum import Enum

class General(Enum):
    RELEASE = False
    ALLOWED_TAGS = ['a', 'b', 'blockquote', 'br', 'em', 'i', 'li', 'ol', 'p', 'strong', 'ul']
    ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'blockquote': ['cite']}