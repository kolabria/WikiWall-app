from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall
from kolabria.appliance.models import Box
from kolabria.walls.forms import NewWallForm, UpdateWallForm, DeleteWallForm
from kolabria.walls.forms import ShareWallForm, ShareUnshareForm, UnshareForm
from mongoengine import StringField
from datetime import datetime

from mongoengine.django.auth import User

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
    form = NewWallForm(request.POST or None)

    if form.is_valid():
        new_wall = Wall.objects.create(owner=request.user,
                                       name=request.POST['name'])
        new_wall.save()
        data = {'title': 'Kolabria', 
                'walls': walls, 
                'new_wall': new_wall,
                'form': form, }
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
def update_sharing(request, wid):
    sharing_form = ShareUnshareForm(request.POST or None)
    wall = Wall.objects.get(id=wid)
    sharing = wall.sharing
    if sharing_form.is_valid():
        messages.info(request, 'wall: %s | %s' % wall.name, wall.id)
        messages.info(request, 'wall.shared: %s ' % ' '.join(sharing))

    data = {'wall': wall,
            'sharing_form': sharing_form,
            'sharing': sharing,
           }

    return render_to_response('walls/share.html', data,
                              context_instance=RequestContext(request))

@login_required
def share_wall(request, wid):
    invite_form = ShareWallForm(request.POST or None)
    wall = Wall.objects.get(id=wid)
    sharing = wall.sharing
    
    if invite_form.is_valid():
        messages.info(request, 'wall: %s | %s' % (wall.name, wall.id))
        messages.info(request, 'invited: %s ' % request.POST['shared'])

        # get latest email and add to walls.sharing if valid
        invited = request.POST['shared'] 
        real = User.objects.filter(email=invited)
        if real and invited not in wall.sharing:
            wall.sharing.append(invited)
            wall.save()
            messages.success(request, '%s appended to wall.sharing for wallid %s' % (invited, wall.id))
            messages.success(request, 'POST wall.sharing: %s' % ', '.join(wall.sharing))
        else:
            messages.warning(request, '%s is not a valid user or has already been added' % invited)

        return HttpResponseRedirect('/walls/share/%s' % wid)
    messages.success(request, 'GET wall.name: %s, wall.id: %s' % (wall.name, wall.id))
    messages.success(request, 'GET wall.sharing: %s' % ' '.join(wall.sharing))

    num_users = len(sharing)
    ShareUnshareFormset = formset_factory(ShareUnshareForm, extra=num_users)
    formset = ShareUnshareFormset()

    share_forms = {}
    count = 0 

    for email in sharing:
        share_forms[formset.forms[count]] 
        count += 1

    data = {'wall': wall, 'form': invite_form, 
            'sharing': sharing, 'share_forms': share_forms,}

    return render_to_response('walls/share.html', data, 
                              context_instance=RequestContext(request))


@login_required
def unshare_wall(request, wid):
    wall = Wall.objects.get(id=wid)
    unshare_form = UnshareForm(request.POST or None)
   
    if request.POST:
#    if unshare_form.is_valid():
        email = request.POST['email']

        if email in wall.sharing:
            wall.sharing.remove(email)
            wall.save()
        
        messages.success(request, 'Success! %s is no longer sharing %s' % (email, wall.name))
        return HttpResponseRedirect('/walls/update/%s' % wid)

    data = {'title': 'Kolabria - Unshare Wall with user',
            'wid': wid,
            'unshare_form': unshare_form, 
            'email': email, }
    return render_to_response('walls/update.html', data,
                              context_instance=RequestContext(request))


@login_required
def update_wall(request, wid):
    # Generate New Wall Form logic but hide form behind modal
    wall = Wall.objects.get(id=wid)
    update_form = UpdateWallForm(request.POST or None)
    update_form.initial['name'] = wall.name
    update_form.fields['published'].label = 'Select one or more appliances to publish your WikiWall'

    unshare_form = UnshareForm(request.POST or None)
    unshare_form.initial['unshared'] = True

    if unshare_form.is_valid():
        email = request.POST['email']
        return HttpResponseRedirect('/walls/update/%s?email=%s' % (wid, email))


    if update_form.is_valid():
        wall.name = request.POST['name']  # update wall name

        # get latest email and add to walls.sharing if valid
        invited = request.POST['invited'] 
        real = User.objects.filter(email=invited)
        if real and invited not in wall.sharing:
            wall.sharing.append(invited)
        wall.save()

        # then update records and publish to selected appliances
        if request.POST['published']:
            published = request.POST['published']

            # update wall.published with appliance ids
            messages.info(request, 'invited: %s | %s | %s ' % (invited, 
                                                               type(invited), 
                                                               len(invited)))
            messages.info(request, 'published: %s | %s | %s ' % (published,
                                                                 type(published), 
                                                                 len(published)))
            messages.info(request, published)
            wall.published.append(published)
            messages.info(request, '%s added to published list on %s (%s)' % (published, wall.name, wall.id))
            box = Box.objects.get(id=published)
            box.walls.append(published)
            box.save()
            wall.save()
            return HttpResponseRedirect('/walls/update/%s' % wid)
#            return render_to_response('walls/update.html', data,
#                              context_instance=RequestContext(request))
        else:
            messages.info(request, 'Updated info for %s' % wall.name)
            return HttpResponseRedirect('/walls/update/%s/' % wid)


    data = {'title': 'Kolabria - Edit Board Details', 
            'wall': wall,
            'update_form': update_form,
            'owner': wall.owner.email,
            'sharing': wall.sharing,
            'unshare_form': unshare_form,
            }

    return render_to_response('walls/update.html', data,
                              context_instance=RequestContext(request))



@login_required
def delete_wall(request, wid):
    del_wall = Wall.objects.get(id=wid)
    del_form = DeleteWallForm(request.POST or None)
    data = {'title': 'Kolabria - Delete Board Confirmation',
            'del_wall': del_wall,
            'del_form': del_form,}
    if del_form.is_valid():
        del_wall.delete()
        return HttpResponseRedirect('/walls/')
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
