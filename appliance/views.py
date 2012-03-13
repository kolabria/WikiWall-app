from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.appliance.models import Box
#from kolabria.walls.forms import NewBoxForm, EditBoxForm, RemoveBoxForm
from datetime import datetime


@login_required
def appliances(request):
    boxes = Box.objects.filter(owner=request.user)
    data = {'title': 'Kolabria - My Appliances',
            'boxes': boxes, }
    render_to_response('appliance/myappliance.html', data,
                       context_instance=RequestContext(request))


def detail(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,}
    render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def register(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Register Applianc',
            'box': box,}
    render_to_response('appliance/register.html', data,
                       context_instance=RequestContext(request))


def pair(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Pair Appliance',
            'box': box,}
    render_to_response('appliance/pair.html', data,
                       context_instance=RequestContext(request))


def edit(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Edit Appliance Details',
            'box': box,}
    render_to_response('appliance/edit.html', data,
                       context_instance=RequestContext(request))


def remove(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Remove Appliance',
            'box': box,}
    render_to_response('appliance/remove.html', data,
                       context_instance=RequestContext(request))



    # Views below this comment are for internal dev and debug purposes only

def the_appliance(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,}
    render_to_response('appliance/the-appliance.html', data,
                       context_instance=RequestContext(request))


def id_appliance(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,}
    render_to_response('apppliance/id-appliance.html', data,
                       context_instance=RequestContext(request))
