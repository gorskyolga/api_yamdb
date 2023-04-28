import datetime as dt
import re

from rest_framework import serializers

from api_yamdb.settings import REGEX_USERNAME, ErrorMessage


def validate_username(value):
    pattern = re.compile(REGEX_USERNAME)
    if value == 'me':
        raise serializers.ValidationError(
            ErrorMessage.USERNAME_ME_DENIED_ERROR)
    if not re.fullmatch(pattern, value):
        raise serializers.ValidationError(
            ErrorMessage.USERNAME_WRONG_REGEX_ERROR)
    return value


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise serializers.ValidationError(ErrorMessage.WRONG_TITLE_YEAR_ERROR)
    return value
