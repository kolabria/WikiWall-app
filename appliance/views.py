from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from kolabria.walls.models import Wall
from kolabria.appliance.models import Box
from kolabria.appliance.forms import PubWallForm, UnsubWallForm
from datetime import datetime

import ipdb

@login_required
def appliances(request):
    boxes = Box.objects.all()
    data = {'title': 'Kolabria - My Appliances',
            'boxes': boxes, }
    return render_to_response('appliance/myappliances.html', data,
                       context_instance=RequestContext(request))


def auth_box(request):
    ipdb.set_trace()
    user_agent = request.META['HTTP_USER_AGENT']
    data = {'title': 'Kolabria - Valid Appliance ',}
    if user_agent[:4] == 'WWA-':
        box_id = user_agent[4:]
        try:
            valid = Box.objects.get(id=box_id)
           # authenticate box as user 
            messages.success(request, 'Valid Appliance ID: %s' % box_id)
            return HttpResponseRedirect('/box/%s/' % box_id)
        except Box.DoesNotExist:
            messages.error(request, 'Appliance %s not recognized' % box_id)
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


def the_box(request, bid):
    ipdb.set_trace()
    unsub_form = UnsubWallForm()
    
    pub_form = PubWallForm()
    box = Box.objects.get(id=bid)
    box_name = box.name
    walls = [ Wall.objects.get(id=wid) for wid in box.walls ]

    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,
            'bid': bid,
            'box_name': box_name, 
            'walls': walls, 
            'unsub_form': unsub_form }

    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def pubwall(request, bid):
#    ipdb.set_trace()
    box = Box.objects.get(id=bid)
    box_name = box.name
    walls = [ Wall.objects.get(id=wid) for wid in box.walls ]

    pub_form = PubWallForm(request.POST or None)

    if pub_form.is_valid():
        wid = request.POST['wid']
        wall = Wall.objects.get(id=wid)
        box = Box.objects.get(id=bid)
        box.active_wall = request.POST['wid']
        box.save()
        messages.success(request, 'Wall: %s Activated on appliance: %s' % \
                                                         (wall.name, box.name))
        return HttpResponseRedirect('/box/%s' % box.id)

    pub_form.initial['publish'] = True 

    data = {'title': 'Kolabria | Publish WikiWall',
            'box': box,
            'bid': bid,
            'box_name': box_name,
            'walls': walls,
            'pub_form': pub_form, }

    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def unsubwall(request, bid):
    box = Box.objects.get(id=bid)
    box_name = box.name
    walls = [ Wall.objects.get(id=wid) for wid in box.walls ]

    unsub_form = UnsubWallForm(request.POST or {'unsub': True })
    if unsub_form.is_valid():
        wid = request.POST['wid']
        wall = Wall.objects.get(id=wid)
        if wid in wall.published:
            wall.published.remove(wid)
            wall.save()
            messages.success(request, 'Box unpublished from wall %s' % \
                                                   (box.name, wall.name))
        box = Box.objects.get(id=bid)
        if bid in box.walls:
            box.walls.remove(bid)
            box.active_wall = ''
            box.save()
            messages.success(request, 'Box %s Unsubscribed from wall: %s' % \
                                                                 (box.name, wid))
        return HttpResponseRedirect('/box/%s' % box.id)

    data = { 'bid': bid, 'unsub_form': unsub_form, 'walls': walls }
    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def id_appliance(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,}
    render_to_response('apppliance/id-appliance.html', data,
                       context_instance=RequestContext(request))
