import re
from django.core.exceptions import ValidationError

from profiles.constants import DIGS


def validate_confirmation_code(pin_code):
    invalid_chars = re.findall(
        fr'{re.escape(DIGS)}', pin_code
    )
    if invalid_chars:
        raise ValidationError(
            f'Forbidden symbols {invalid_chars}'
        )
    return pin_code
