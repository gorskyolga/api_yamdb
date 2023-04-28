import re

from rest_framework import serializers


def validate_username(value):
    # шаблон строки для проверки, что строка состоит только из
    # символов, цифр и символов @/./+/-/
    SAMPLE = r'^[\w.@+-]+\Z'

    pattern = re.compile(SAMPLE)
    if value == 'me':
        raise serializers.ValidationError(
            'Использование значения "me" в качестве `username` запрещено!')
    elif not re.fullmatch(pattern, value):
        raise serializers.ValidationError(
            f'Значение `username` не удовлетворяет шаблону "{SAMPLE}"!')
    return value
