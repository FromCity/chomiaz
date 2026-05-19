from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_external_message_id(data):
    if 'external_message_id' in data :
        raise ValidationError(
            _("the external_message_id field is missing"),
            params={"data": data},
            )

def validate_text(text):
    if len(text) == 0:
        raise ValidationError(
            _("text not be empty"),
            params={"data": text},
            )