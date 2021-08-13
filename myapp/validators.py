import re

from django.core.exceptions import ValidationError


def not_only_numeric_validator(value):
    if value.isnumeric():
        raise ValidationError('This field cannot contain only numeric characters.')
    return value


def no_special_characters_validator(value):
    if not bool(re.match(r'^[A-Za-z0-9]*$', value)):
        raise ValidationError('Todo title can only contain letters and numbers.')