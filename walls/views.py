from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall
from kolabria.walls.forms import NewWallForm

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
def view_wall(request, wid):
    wall = Wall.objects.filter(id=wid)
    data = {'title': 'Kolabria',
            'wall': wall,}
    return render_to_response('walls/wall.html', data, 
                              context_instance=RequestContext(request))

@login_required
def thewall(request):
    wall = Wall.objects.get(id='4f562576e857721363000000')
    data = {'title': 'Kolabria',
            'wall': wall,}
    return render_to_response('walls/wall.html', data, 
                              context_instance=RequestContext(request))


@login_required
def create_wall(request):
    if request.method == 'GET':
        form = NewWallForm()
    else:
        form = NewWallForm(request.POST)
        if form.is_valid():
            new_wall = Wall.objects.create(owner=request.user,
                                           name=request.POST['name'])
            new_wall.save()
            data = {'title': 'Kolabria', 'wall': new_wall,}
            return render_to_response('walls/created.html', data,
                              context_instance=RequestContext(request))

    data = {'title': 'Kolabria', 'form': form }
    return render_to_response('walls/create.html', data,
                              context_instance=RequestContext(request))

@login_required
def created_wall(request):

    data = {'title': 'Kolabria', }
    return render_to_response('walls/created.html', data, 
                              context_instance=RequestContext(request))

@login_required
def delete_wall(request):
    pass
