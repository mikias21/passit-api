from enum import Enum

class CategoryErrorMessages(Enum):
    CATEGORY_NOT_FOUND = "Category not found in our records."
    INVALID_CATEGORY_NAME = "Category name can only be letters and numbers."
    CATEGORY_DUPLICATE = "You have already created this category."