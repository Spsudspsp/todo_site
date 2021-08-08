from django.core.exceptions import ValidationError


def not_only_numeric_validator(value):
    if value.isnumeric():
        raise ValidationError('This field cannot contain only numeric characters.')
    return value
