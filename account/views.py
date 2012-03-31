from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from kolabria.account.forms import NewAccountForm
from mongoengine.django.auth import User

import ipdb

def create(request):
    form = NewAccountForm(request.POST or None)
    if form.is_valid():
        messages.success(request, request.POST)
        return HttpResponseRedirect('/walls/')

    data = {'title': 'Kolabria - Create a new Account ', 'form': form, }
    return render_to_response('account/register.html', data,
                              context_instance=RequestContext(request))


