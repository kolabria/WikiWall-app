from crispy_forms.helpers import FormHelper
from crispy_forms.layout import Submit

from bootstrap.forms import BootstrapForm, Fieldset
from mongoengine.django.auth import User
from mongoengine import EmailField

#from mongoforms import MongoForm
from kolabria.walls.models import Wall
from kolabria.appliance.models import Box


from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe 
from django import forms

class NewWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please enter details", "name", "description", ),
        )
    name = forms.CharField(max_length=30, required=True)


class DeleteWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please Confirm Delete", "confirmation", ),
        )
    confirmed = forms.BooleanField(initial=False, required=True)

class EditWallForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset("Please update details", "name", "description", ),
        )
    name = forms.CharField(max_length=30, required=True)

class ShareWallForm(forms.Form):
    shared = forms.EmailField(widget=forms.TextInput(
                              attrs={'placeholder': 'email@address.com'}), 
                              max_length=60, required=True)


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class ShareUnshareForm(forms.Form):
    CHOICES = (('0', 'Unshare'), ('1', 'Share'))
    shared = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect(
                                   renderer=HorizontalRadioRenderer)
                              )
#attrs={'placeholder': '1', 'class': 'button-group btn', 'data-toggle':'buttons-radio'}

class UpdateWallForm(forms.Form):
    OPTIONS = ()
    boxes_available = Box.objects.all()
    for box in boxes_available:
        OPTIONS += ( box.id, box.name),
    name = forms.CharField(widget=forms.TextInput(),max_length=30, required=True)
    invited = forms.EmailField(widget=forms.TextInput(
                               attrs={'placeholder':'email@address.com'}),
                               required=False)
    published = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={}), 
                                          choices=OPTIONS, required=False)
