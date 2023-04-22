import re

from rest_framework import serializers


def validate_username(value):
    pattern = re.compile(r'^[\w.@+-]+\Z')
    if value == 'me':
        raise serializers.ValidationError(
            'Использование значения "me" в качестве `username` запрещено!')
    elif not re.fullmatch(pattern, value):
        raise serializers.ValidationError(
            r'Значение `username` не удовлетворяет шаблону "^[\w.@+-]+\Z"!')
    return value
