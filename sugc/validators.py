import datetime

from django.core.validators import ValidationError


def not_in_past_validator(date):
    if datetime.date.today() >= date:
        raise ValidationError(
            "Date must be in future!"
        )
