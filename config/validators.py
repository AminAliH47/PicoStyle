from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

phone_regex = RegexValidator(regex='^[ 0-9]+$',
                             message=_("Your entered phone number is not valid"))

number_regex = RegexValidator(regex='^[ 0-9]+$',
                              message=_("Please enter a valid number"))


def validate_file_size(value):
    file_size = value.size

    if file_size > 1621440:
        raise ValidationError(_("The maximum size for uploading photos is 1.5 MB"))
    else:
        return value
