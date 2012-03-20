from bootstrap.forms import BootstrapForm, Fieldset
from mongoengine.django.auth import User
from mongoengine import EmailField
from django import forms

class NewWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please enter details", "name", "description", ),
        )
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=256, required=False)


class EditWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please update details", "name", "description", ),
        )
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=256, required=False)

class DeleteWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please Confirm Delete", "confirmation", ),
        )
    confirmation = forms.BooleanField(False)

class ShareWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Invite users by email", "name", ),
        )
    shared = forms.EmailField(max_length=60, required=True)


class UpdateWallForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    invited = forms.EmailField(max_length=60, required=False)
