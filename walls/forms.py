from crispy_forms.helpers import FormHelper
from crispy_forms.layout import Submit

from bootstrap.forms import BootstrapForm, Fieldset
from mongoengine.django.auth import User
from mongoengine import EmailField

from mongoforms import MongoForm
from kolabria.walls.models import Wall
from django import forms


class NewWallForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input = 'Enter a Name'
        self.helper.form_method = 'post'
        self.helper.form_action = 'create_wall'
        self.helper.form_class = 'form-horizontal'
    name = forms.CharField()

class DeleteWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please Confirm Delete", "confirmation", ),
        )
    confirmed = forms.BooleanField(initial=False, required=True)

"""
class NewWallForm(MongoForm):
    class Meta:
        document = Wall
        field = ('name',)
    name =  forms.CharField(widget=forms.Textarea)

class NewWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please enter details", "name", "description", ),
        )
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=256, required=False)

class DeleteWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please Confirm Delete", "confirmation", ),
        )
    confirmation = forms.BooleanField(initial=False, required=True)
"""

class EditWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please update details", "name", "description", ),
        )
    name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=256, required=False)
class ShareWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Invite users by email", "name", ),
        )
    shared = forms.EmailField(max_length=60, required=True)


class UpdateWallForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    invited = forms.EmailField(max_length=60, required=False)
