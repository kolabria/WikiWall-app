from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kolabria.account.forms import NewAccountForm, NewBoxForm
from kolabria.account.models import Account
from kolabria.appliance.models import Box
from mongoengine.django.auth import User

import ipdb


def create(request):
    form = NewAccountForm(request.POST or None)
    if form.is_valid():
        # create the account instance
        new_account = Account()
        new_account.name = request.POST['company_name']
        new_account.phone = request.POST['phone']
        new_account.address1 = request.POST['address1']
        new_account.address2 = request.POST['address2']
        new_account.city = request.POST['city']
        new_account.state = request.POST['state']
        new_account.postal_zip = request.POST['postal_zip']
        new_account.country = request.POST['country']
        new_account.save()
        messages.success(request, new_account)

        # create new user and save profile details; save new user
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password2']
        new_user = User.create_user(username=username, email=email,
                                    password=password)
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST['last_name']
        new_user.save()

        # set new user as admin for account instance; save account
        new_account.admin = new_user
        new_account.save()

        # authenticate and log in user
        auth_user = authenticate(username=username, password=password)
        login(request=request, user=auth_user)
        messages.success(request, 'Successfully logged in as %s' % \
                                                           auth_user.username)
        return HttpResponseRedirect('/welcome/')

    data = {'title': 'Kolabria - Create a new Account ', 'form': form,
             }
    return render_to_response('account/create.html', data,
                              context_instance=RequestContext(request))


def public(request):
    data = {'title': 'Kolabria - Homepage', }
    return render_to_response('public/home.html', data,
                              context_instance=RequestContext(request))


