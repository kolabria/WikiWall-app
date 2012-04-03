from mongoengine.django.auth import User
from kolabria.appliance.models import Box
from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USStateSelect
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django import forms

class NewAccountForm(forms.Form):
    company_name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Company Name',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    first_name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'First Name',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    last_name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Last Name',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    email = forms.EmailField(widget=forms.TextInput(
                           attrs={'placeholder': 'first.last@company.com',
                                  'class': 'span4'}),
                           max_length=30,
                           required=True)
    phone = USPhoneNumberField(widget=forms.TextInput(
                           attrs={'placeholder': '555-875-1000',
                                  'class': 'span4'}))
    address1 = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': '123 4th Avenue, Suite 1215',
                                  'class': 'span4'}),
                           max_length=80, 
                           required=True)
    address2 = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': '12th Floor Receiving',
                                  'class': 'span4'}),
                           max_length=80, 
                           required=False)
    city = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Springfield',
                                  'class': 'span4'}),
                           max_length=64, 
                           required=True)
    state = USStateField(widget=USStateSelect)
    postal_zip = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': '',
                                  'class': 'span4'}),
                           max_length=6,
                           required=True)
    country = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'USA',
                                  'class': 'span4'}),
                           max_length=30,
                           required=True)
