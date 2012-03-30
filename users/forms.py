from django import forms
from mongoengine.django.auth import User

class UserDetailsForm(forms.Form):
    """
    A form that updates a user's First and Last Name, email address and other"
    optional details
    """
    first_name = forms.CharField(widget=forms.TextInput(
                                 attrs={'placeholder': 'First Name',
                                         'class': 'span4'}),
                                 max_length=30, required=False)
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={'placeholder': 'Last Name',
                                       'class': 'span4'}),
                                max_length=30, required=False)
#    email = forms.EmailField(widget=forms.TextInput(
#                             attrs={'placeholder': 'Last Name',
#                                    'class': 'span4'}),
#                             required=True)
