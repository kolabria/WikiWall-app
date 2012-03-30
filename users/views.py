from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kolabria.users.forms import UserDetailsForm

from mongoengine.django.auth import User
from kolabria.users.models import UserProfile

import ipdb

@login_required
def profile(request):
    user = request.user
    details_form = UserDetailsForm(request.POST or None)
    if details_form.is_valid():
        first = request.POST['first_name']
        last = request.POST['last_name']
        messages.info(request, '%s %s' % (first, last))
        user.first_name = first
        user.last_name = last
        user.save()
        full_name = '%s %s %s' % (user.first_name, user.last_name, user.email)
        messages.success(request, 'Updated user details for %s' % full_name)
        return HttpResponseRedirect('/profile/')

    data = {'title': 'Kolabria - Edit Profile', 'details_form': details_form, }
    return render_to_response('users/profile.html', data,
                              context_instance=RequestContext(request))
