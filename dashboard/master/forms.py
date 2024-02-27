from dataclasses import fields
import email

from django import forms
from django.contrib.auth.models import User

from django.forms import ModelForm
from pkg_resources import require

class UserForm(ModelForm):
    first_name = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'class' : 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'class' : 'form-control'})
    )
    email = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'class' : 'form-control'})
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        