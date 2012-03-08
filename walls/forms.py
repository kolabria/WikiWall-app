from django import forms
from mongoengine.django.auth import User


class NewWallForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=256, required=False)
