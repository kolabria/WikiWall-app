from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall
from kolabria.walls.forms import NewWallForm, EditWallForm, DeleteWallForm
from kolabria.walls.forms import ShareWallForm
from mongoengine import StringField
from datetime import datetime

@login_required
def walls(request):
    # Generate New Wall Form logic but hide form behind modal
    walls = Wall.objects.filter(owner=request.user)
    shared_walls = Wall.objects.filter(sharing=request.user.email)
    data = {'title': 'Kolabria', 
            'walls': walls, 
            'shared_walls': shared_walls,
            }
    return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))

@login_required
def create_wall(request):
    walls = Wall.objects.filter(owner=request.user)
    if request.method == 'GET':
        form = NewWallForm()
    else:
        form = NewWallForm(request.POST)
        if form.is_valid():
            new_wall = Wall.objects.create(owner=request.user,
                                           name=request.POST['name'],
                                           description=request.POST['description'])
            new_wall.save()
            data = {'title': 'Kolabria', 
                    'walls': walls, 
                    'new_wall': new_wall,}
            return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))

    data = {'title': 'Kolabria', 'form': form }
    return render_to_response('walls/create.html', data,
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
def share_wall(request, wid):
    form = ShareWallForm(request.POST or None)
    wall = Wall.objects.get(id=wid)
    sharing = wall.sharing
#    viewing = wall.viewing
    data = {'title': 'Kolabria',
            'wall': wall,
            'form': form,
            'sharing': sharing,
          #  'viewing': viewing,
           }

    if form.is_valid():
        wall.sharing.append(request.POST['shared'])
        if request.POST['unshare']:
            wall.sharing.remove(request.POST['unshare'])
        wall.save()
        return render_to_response('walls/share.html', data,
                                  context_instance=RequestContext(request))
    return render_to_response('walls/share.html', data, 
                              context_instance=RequestContext(request))


@login_required
def unshare_wall(request, wid, email):
    wall = Wall.objects.get(id=wid)
    data = {'title': 'Kolabria - Unshare Wall with user',
            'wid': wid,
            'email': email,
           }
    if email in wall.sharing:
        wall.sharing.remove(email)
        wall.save()
    return render_to_response('walls/share.html', data,
                              context_instance=RequestContext(request))


@login_required
def edit_wall(request, wid):
    # Generate New Wall Form logic but hide form behind modal
    edit_wall = Wall.objects.get(id=wid)
    walls = Wall.objects.filter(owner=request.user)
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
            data = {'title': 'Kolabria - Edit Board Details', 
                    'walls': walls, 
                    'edit_wall': edit_wall,}
            return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))
    data = {'title': 'Kolabria - Update Board Details - Input Form', 
            'edit_form': edit_form,
            }
    return render_to_response('walls/update.html', data,
          context_instance=RequestContext(request))


@login_required
def delete_wall(request, wid):
    del_wall = Wall.objects.get(id=wid)
    data = {'title': 'Kolabria - Delete Board Confirmation',
            'del_wall': del_wall,}
    if request.method == 'GET':
        del_form = DeleteWallForm()
        data['del_form'] = del_form
    else:  # handle 'POST' in request
        checkbox = request.POST['confirmation']
        if checkbox:
            walls = Wall.objects.filter(owner=request.user)
            deleted_wall = del_wall
            del_wall.delete()
            request.session['deleted_wall'] = deleted_wall
            data = {'deleted_wall': deleted_wall,
                    'walls': walls,}
            return HttpResponseRedirect('/walls/')

        else:
            pass
            #TODO add else logic to handle no confirmation selected
    return render_to_response('walls/delete.html', data,
                              context_instance=RequestContext(request))

# Remaining Views are for internal dev and debug use only 

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
