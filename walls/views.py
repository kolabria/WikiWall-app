from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall

@login_required
def mongo_walls(request):
    walls = Wall.objects.filter(owner=request.user)
    data = {'title': 'Kolabria - My Whiteboards',
            'walls': walls,}
    return render_to_response('mongo/mywalls.html', data,
                              context_instance=RequestContext(request))

@login_required
def my_walls(request):
    data = {'title': 'Kolabria - My Whiteboards', }
    return render_to_response('mongo/mywalls.html', data,
                              context_instance=RequestContext(request))


@login_required
def view_wall(request, link):
    wall = Wall.objects.filter(link=link)[0]
    data = {'title': 'Kolabria',
            'wall': wall,}
    return render_to_response('walls/wall.html', data, 
                              context_instance=RequestContext(request))
