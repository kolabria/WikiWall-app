from django import forms
from mongoengine.django.auth import User


class NewWallForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=256, required=False)


class EditWallForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=256, required=False)

class DeleteWallForm(forms.Form):
    confirmation = forms.BooleanField(False)
