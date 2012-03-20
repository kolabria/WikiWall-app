from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall
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


def route_box(request):
    user_agent = request.META['HTTP_USER_AGENT']
    data = {'title': 'Kolabria - Appliance Dashboard',}
    if user_agent[:4] == 'WWA-':
        box_id = user_agent[4:]
        data['box_id'] = box_id
        return render_to_response('appliance/dashboard.html', data,
                           context_instance=RequestContext(request))
    return HttpResponseRedirect('/')

    # Views below this comment are for internal dev and debug purposes only

def the_box(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    walls = [ Wall.objects.get(id=wid) for wid in box.walls ]
#    walls = [ Wall.objects(published=wall_id) for wall_id in box.walls ]
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,
            'box_id': box_id,
            'box_name': box_name, 
            'walls': walls, }
    return render_to_response('appliance/detail.html', data,
                       context_instance=RequestContext(request))


def id_appliance(request, box_id):
    box = Box.objects.get(id=box_id)
    box_name = box.name
    data = {'title': 'Kolabria | Manage Appliances | Appliance Detail',
            'box': box,}
    render_to_response('apppliance/id-appliance.html', data,
                       context_instance=RequestContext(request))
