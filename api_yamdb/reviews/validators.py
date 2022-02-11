from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError('Год выпуска произведения превышает текущий.')

    if value < 1900:
        raise ValidationError('Выберите произведения, изданные после 1900г.')
