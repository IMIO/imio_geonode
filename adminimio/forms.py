# -*- coding: utf8 -*-
from django import forms
from django.core.validators import validate_email, ValidationError
from slugify import slugify
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model


class ValidFormUpdatelayer(forms.Form):
    csrf_token = forms.CharField()

class ValidFormCommuneUser(forms.Form):
    csrf_token = forms.CharField()
    in_user = forms.CharField()
    in_comm = forms.CharField()




