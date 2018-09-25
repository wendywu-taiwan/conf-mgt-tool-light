from django import forms
from django.core import validators
from django.db.models import TextField
from rest_framework.fields import ListField


class LongURLField(TextField):
    description = 'Long URL'

    def __init__(self, verbose_name=None, name=None, **kwargs):
        TextField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(validators.URLValidator())

    def formfield(self, **kwargs):
        # As with TextField, this will cause URL validation to be performed
        # twice.
        defaults = {
            'form_class': forms.URLField,
        }
        defaults.update(kwargs)
        return super(LongURLField, self).formfield(**defaults)


class StringArrayField(ListField):
    def to_internal_value(self, data):
        data = data.split(",")  # convert string to list
        return super().to_internal_value(self, data)
