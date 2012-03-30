from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kolabria.walls.forms import NewWallForm, UpdateWallForm, DeleteWallForm
from kolabria.walls.forms import ShareWallForm, UnshareWallForm
from kolabria.walls.forms import PubWallForm, UnpubWallForm 

from mongoengine.django.auth import User
from kolabria.walls.models import Wall
from kolabria.appliance.models import Box

import ipdb

@login_required
def profile(request):
    user = request.user
    data = {'title': 'Kolabria - Edit Profile', }

    return render_to_response('users/profile.html', data,
                              context_instance=RequestContext(request))
