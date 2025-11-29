from django import forms
from django.core.exceptions import ValidationError


def start_with_0(value):
    
    if value[0] != 0:
        raise ValidationError("the phone number must be start with 0 number", code='invalid_phone_number')