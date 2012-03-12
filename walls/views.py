from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from kolabria.walls.models import Wall
from kolabria.walls.forms import NewWallForm, EditWallForm, DeleteWallForm
from datetime import datetime

@login_required
def modal(request):
    # Generate New Wall Form logic but hide form behind modal
    if request.method == 'GET':
        new_form = NewWallForm()
        edit_form = EditWallForm()
        del_form = DeleteWallForm()
    else:  # request.method == 'POST'
        new_form = NewWallForm(request.POST)
        if new_form.is_valid():
            new_wall = Wall.objects.create(owner=request.user,
                                           name=request.POST['name'])
            new_wall.save()
            data = {'title': 'Kolabria', 'wall': new_wall,}
            return render_to_response('walls/created.html', data,
                              context_instance=RequestContext(request))

    # Get walls page with modal pop-up
    walls = Wall.objects.filter(owner=request.user)
    data = {'title': 'Kolabria', 
            'new_form': new_form,
            'edit_form': new_form,
            'del_form': new_form,
            'walls': walls, }
    return render_to_response('walls/modal.html', data,
                              context_instance=RequestContext(request))

@login_required
def create_msg(request):
    # Get walls page with modal pop-up
    walls = Wall.objects.filter(owner=request.user)
    messages.success(request, 'message updated.')
    data = {'title': 'Kolabria', 
            'walls': walls, }
    return render_to_response('walls/modal.html', data,
                              context_instance=RequestContext(request))



@login_required
def new_wall(request):
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
    return render_to_response('walls/modal.html', data,
                              context_instance=RequestContext(request))


@login_required
def walls(request):
    # Get walls for this user
    walls = Wall.objects.filter(owner=request.user)
    data = {'title': 'Kolabria - My Whiteboards',
            'walls': walls,}
    return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))

@login_required
def view_wall(request, wid):
    # Get a specific wall by Mongo object id
    wall = Wall.objects.get(id=wid)
    data = {'title': 'Kolabria',
            'wall': wall,}
    return render_to_response('walls/newwall.html', data, 
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
def edit_wall(request, wid):
    # Generate New Wall Form logic but hide form behind modal
    edit_wall = Wall.objects.get(id=wid)
    if request.method == 'GET':
        edit_form = EditWallForm()
        edit_form.initial['name'] = edit_wall.name
        edit_form.initial['description'] = edit_wall.description
    else:  # request.method == 'POST'
        edit_form = EditWallForm(request.POST)
        if edit_form.is_valid():
            edit_wall['name'] = request.POST['name']
            edit_wall['description'] = request.POST['description']
            edit_wall['modified'] = datetime.now()
            edit_wall.save()
            data = {'title': 'Kolabria', 'edit_form': edit_wall,}
            messages.success(request, 'Board details updated.')
            return render_to_response('walls/modal.html', data,
                              context_instance=RequestContext(request))
    data = {'title': 'Kolabria', 
            'edit_form': edit_form,
            'walls': walls, }
    return render_to_response('walls/update.html', data,
          context_instance=RequestContext(request))


@login_required
def delete_wall(request):
    pass


@login_required
def idwall(request):
    wall = Wall.objects.get(id='4f562576e857721363000000')
    data = {'title': 'Kolabria',
            'wall': wall,}
    return render_to_response('walls/idwall.html', data, 
                              context_instance=RequestContext(request))


@login_required
def thewall(request):
    wall = Wall.objects.get(id='4f562576e857721363000000')
    data = {'title': 'Kolabria',
            'wall': wall,}
    return render_to_response('walls/thewall.html', data, 
                              context_instance=RequestContext(request))
