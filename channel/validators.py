from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


def validate_tag(value):
    if not value.startswith('#'):
        raise ValidationError('As tags devem começar com #')
    return value
