import re

from rest_framework.exceptions import ValidationError


def username_validator(username):
    pattern = re.compile(r"^[\w.@+-]+$")
    if pattern.match(username):
        return username
    raise ValidationError("Incorrect username")
