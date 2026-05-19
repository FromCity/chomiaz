from django import forms
from .validators import validate_external_message_id, validate_text


class DataForm(forms.Form):
    external_message_id = forms.CharField()
    user_id =  forms.CharField()
    text = forms.CharField(validators=[validate_text])
    created_at = forms.DateTimeField()
