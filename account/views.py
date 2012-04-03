from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from kolabria.account.forms import NewAccountForm
from kolabria.account.models import Account
from mongoengine.django.auth import User

import ipdb

def create(request):
    form = NewAccountForm(request.POST or None)
    if form.is_valid():
        new_account = Account()
        new_account.company = request.POST['company_name']
        new_account.first_name = request.POST['first_name']
        new_account.last_name = request.POST['last_name']
        new_account.email = request.POST['email']
        new_account.phone = request.POST['phone']
        new_account.address1 = request.POST['address1']
        new_account.address2 = request.POST['address2']
        new_account.city = request.POST['city']
        new_account.state = request.POST['state']
        new_account.postal_zip = request.POST['postal_zip']
        new_account.country = request.POST['country']
        new_account.save()
        messages.success(request, request.POST)
        messages.success(request, new_account)
        return HttpResponseRedirect('/account/create/')

    data = {'title': 'Kolabria - Create a new Account ', 'form': form, }
    return render_to_response('account/create.html', data,
                              context_instance=RequestContext(request))

"""
def register(request):
    form = UserCreationForm(request.POST or None)
    data = {'title': 'Kolabria - Registration Page',
            'form': form,}
    if form.is_valid():
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password2']
        new_user = User.create_user(username=username, email=email,
                                    password=password)
        new_user.save()
        auth_user = authenticate(username=username, password=password)
        login(request=request, user=auth_user)
        return render_to_response('login/register-success.html',
                          context_instance=RequestContext(request))
    return render_to_response('login/register.html', data,
                              context_instance=RequestContext(request))
"""
