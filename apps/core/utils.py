from django.core.validators import RegexValidator
from django.utils.translation import gettext, gettext_lazy as _


class UsernameValidator(RegexValidator):
    regex = r"^[\w]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, numbers, and _ character."
    )
    flags = 0


class TwitterUsernameValidator(RegexValidator):
    regex = r"^@[\w]+\Z"
    message = _(
        "Enter a valid Twitter username. This value may start with @ and contain only letters, numbers, and _ character."
    )
    flags = 0
