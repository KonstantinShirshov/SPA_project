from rest_framework.serializers import ValidationError
import re

url_patterns = [
    r'^(https?://)?(www\.)?youtube\.com/.+$',
    r'^(https?://)?(www\.)?youtu\.be/.+$'
]


def validate_youtube_url(value):
    """ Проверяет, что в переданном тексте нет ссылок, кроме youtube.com или youtu.be. """

    for pattern in url_patterns:
        if re.match(pattern, value):
            return value

    raise ValidationError("Поле «видео» должно содержать ссылку на YouTube.")
