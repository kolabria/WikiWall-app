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


class NewWallForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Name this Wikiwall',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    invited = forms.EmailField(widget=forms.TextInput(
                               attrs={'placeholder':'email@address.com',
                                      'class': 'span8'}),
                               required=False)


class DeleteWallForm(forms.Form):
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

class UnshareForm(forms.Form):
    unshared = forms.BooleanField(widget=forms.CheckboxInput,
                                  label='Unshare',
                                  )
    email = forms.EmailField(widget=forms.HiddenInput)


class UnpublishWallForm(forms.Form):
    unpublished = forms.BooleanField(widget=forms.CheckboxInput,
                                  label='Unshare')
    box = forms.CharField(widget=forms.HiddenInput,
                          max_length=128)

class UpdateWallForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                           attrs={'class': 'span8'}), 
                           max_length=30, required=True)
    invited = forms.EmailField(widget=forms.TextInput(
                               attrs={'placeholder':'email@address.com',
                                      'class': 'span8'}),
                               required=False)

#    def clean_invited(self):
#        invited = self.cleaned_data['invited']
#        try:
#            real = User.objects.filter(email=invited)
#        except real.DoesNotExist:
#            return self.cleaned_data['invited'] 
#        raise forms.ValidationError(invited)
#        raise forms.ValidationError("Sorry, %s is not a valid user. Please try again" % invited)



class PubishWallForm(forms.Form):
    OPTIONS = ()
    boxes_available = Box.objects.all()
    for box in boxes_available:
        OPTIONS += ( box.id, box.name ),
    published = forms.MultipleChoiceField(widget=forms.SelectMultiple(
                                          attrs={'class': 'span4'}),
                                          choices=OPTIONS,
                                          required=False)
