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


def route_box(request):
    user_agent = request.META['HTTP_USER_AGENT']
    data = {'title': 'Kolabria - Appliance Dashboard',}
    if user_agent[:4] == 'WWA-':
        box_id = user_agent[4:]
        return HttpResponseRedirect('/box/%s' % box_id)
    return HttpResponseRedirect('/')


def the_box(request, bid):
#    ipdb.set_trace()
    unsub_form = UnsubWallForm()
    
    pub_form = PubWallForm()

    box = Box.objects.get(id=bid)
    box_name = box.name
    walls = Wall.objects.filter(published=str(box.id))

    if box.active_wall:
        active = Wall.objects.get(id=box.active_wall)
    else:
        active = None

    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,
            'bid': bid,
            'active': active,
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
    unsub_form = UnsubWallForm(request.POST or None)
    if unsub_form.is_valid():
        box = Box.objects.get(id=bid)
        wid = request.POST.get('wid')
        wall = Wall.objects.get(id=wid)
        if bid in wall.published:
            wall.published.remove(bid)
            wall.save()
            messages.success(request, 'Box %s removed from wall.published %s' % \
                                                                  (box.name, wall.name))
        box = Box.objects.get(id=bid)
        if wid in box.walls:
            box.walls.remove(wid)
            box.active_wall = ''
            box.save()
            messages.success(request, 'Box %s Unsubscribed from box.wall: %s' % \
                                                                 (box.name, wid))
        return HttpResponseRedirect('/box/')
    
    data = { 'bid': bid, 'unsub_form': unsub_form } #, 'walls': walls }
    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def id_appliance(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'bux': box,}
    render_to_response('apppliance/id-appliance.html', data,
                       context_instance=RequestContext(request))
