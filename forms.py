from django import forms
from mongoengine.django.auth import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
                                          
                        
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    company = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text = "Enter the same password as above, for verification.")
    terms_of_service = forms.CheckboxInput()
