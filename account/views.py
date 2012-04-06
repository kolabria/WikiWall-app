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

@login_required
def welcome(request):
    form = NewBoxForm(request.POST or None)
    if form.is_valid():
        name = request.POST['name']
        location = request.POST['location']
        box = Box.objects.create(name=name, location=location)
        box.save()
        msg = '%s %s %s' % (box.id, box.name, box.location)
        messages.info(request, msg)
        messages.info(request, request.POST)
        return HttpResponseRedirect('/welcome/')

    data = {'title': 'Kolabria - New Account Confirmation', 'form': form, }
    return render_to_response('account/welcome.html', data,
                              context_instance=RequestContext(request))
