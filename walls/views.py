from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall
from kolabria.appliance.models import Box
from kolabria.walls.forms import NewWallForm, UpdateWallForm, DeleteWallForm
from kolabria.walls.forms import ShareWallForm, ShareUnshareForm, UnshareForm
from kolabria.walls.forms import UnpublishWallForm
#from kolabria.walls.forms import PublishWallForm

from mongoengine import StringField
from datetime import datetime

from mongoengine.django.auth import User

# Legend of urls and views
#walls             url(r'^walls/$', views.walls), 
#create_wall       url(r'^walls/create/$', views.create_wall),
#view_wall         url(r'^walls/share/(?P<wid>\w+)/$', views.share_wall),
#update_sharing    #
#share_wall        url(r'^walls/unpublish/(?P<wid>\w+)/$', views.unshare_wall),
#unshare_wall      url(r'^walls/unshare/(?P<wid>\w+)/$', views.unshare_wall),
#update_wall       url(r'^walls/update/(?P<wid>\w+)/$', views.update_wall),
#delete_wall       url(r'^walls/delete/(?P<wid>\w+)/$', views.delete_wall),
#idwall            url(r'^idwall/$', views.idwall),
#thewall           url(r'^thewall/$', views.thewall),

@login_required
def walls(request):
    # Generate New Wall Form logic but hide form behind modal
    new_wall_form = NewWallForm(request.POST or None)
    new_wall_form.fields['name'].label = 'Enter WikiWall Name'
    invited_label = 'Invite users by email address separate by commas.'
    new_wall_form.fields['invited'].label = invited_label

    del_form = DeleteWallForm(request.POST or None)
    del_form.fields['confirmed'].label = ''
    del_form.initial['confirmed'] = True

    if new_wall_form.is_valid():
        wall = Wall.objects.create(owner=request.user,
                                   name=request.POST['name'])
        if request.POST.get('invited', ''):
            invited = request.POST['invited'] 
            raw_emails = invited.split(',')
            clean_emails = [ email.strip() for email in raw_emails ]
            for email in clean_emails:
                try:
                    real = User.objects.get(email=email)
                    if email not in wall.sharing:
                        wall.sharing.append(email)
                    else:
                        messages.warning(request, '%s is already sharing' % email)
                except DoesNotExist:
                    messages.warning(request, 'User with email %s not valid. Try again.')
                messages.info(request, 'Successfully added: %s' % email)
        wall.save()
        wid = wall.id
        messages.success(request, 'Successfully created Wall: %s - %s' % \
                                                              (wid, wall.name))
        return HttpResponseRedirect('/walls/')

    own = Wall.objects.filter(owner=request.user)
    shared = Wall.objects.filter(sharing=request.user.email)
    walls = {'own': own, 'shared': shared,}

    data = {'title': 'Kolabria', 
            'walls': walls, 
#            'shared_walls': shared_walls,
            'new_wall_form': new_wall_form,
            'del_form': del_form,
            }
    return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))


@login_required
def modal(request):
    walls = Wall.objects.filter(owner=request.user)
    data = {'title': 'Kolabria', 
            'walls': walls, }
    return render_to_response('walls/modal.html', data,
                              context_instance=RequestContext(request))


@login_required
def create_wall(request):
    form = NewWallForm(request.POST or None)
    form.fields['name'].label = 'Enter WikiWall Name'
    form.fields['invited'].label = 'Invite users by email'

    if form.is_valid():
        wall = Wall.objects.create(owner=request.user,
                                   name=request.POST['name'])
        if request.POST.get('invited', ''):
            invited = request.POST['invited'] 
            real = User.objects.filter(email=invited)
            if real and invited not in wall.sharing:
                wall.sharing.append(invited)
            messages.info(request, 'invited: %s' % invited)
        wall.save()
        wid = wall.id
        messages.success(request, 'Successfully created Wall: %s - %s' % \
                                                              (wid, wall.name))
        return HttpResponseRedirect('/walls/')



    data = {'title': 'Kolabria - Create a new WikiWall',
            'form': form }
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
def delete_wall(request, wid):
    del_wall = Wall.objects.get(id=wid)
    del_form = DeleteWallForm(request.POST or None)
    del_form.fields['confirmed'].label = 'Confirm WikiWall Deletion'
    data = {'title': 'Kolabria - Delete Board Confirmation',
            'del_wall': del_wall,
            'del_form': del_form,}
    if del_form.is_valid():
        confirmed = request.POST.get('confirmed')
        del_wall_name = del_wall.name
        del_wall.delete()
        messages.info(request, 'Test Confirmed: Confirmed=%s for Wall Name: %s' % (confirmed, del_wall_name))
        messages.success(request, 'Successfully deleted WikiWall - %s' % del_wall_name)
        return HttpResponseRedirect('/walls/')
    
    return render_to_response('walls/delete.html', data,
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
def unpublish_wall(request, wid):
    wall = Wall.objects.get(id=wid)
    unpublish_form = UnpublishWallForm(request.POST or None)
   
    if unpublish_form.is_valid():
        email = request.POST['email']
        if email in wall.sharing:
           wall.sharing.remove(email)
           wall.save()
           messages.success(request, 'Success! %s is no longer sharing %s' % (email, wall.name))
        messages.warning(request, 'Error: %s does not have access to wall: %s.' % (email, wall.name))
    return HttpResponseRedirect('/walls/update/%s' % wid)

    data = {'title': 'Kolabria - Unshare Wall with user',
            'wid': wid,
            'unshare_form': unshare_form, 
            'email': email, }
    return render_to_response('walls/update.html', data,
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
    wall = Wall.objects.get(id=wid)

    unpublish_form = UnpublishWallForm(request.POST or None)
    if unpublish_form.is_valid():
        unpublish = request.POST['published']
        messages.debug(request, 'unpublish request for %s' % unpublish)
        return HttpResponseRedirect('/walls/unpublish/%s' % wid)
    unpublish_form.initial['published'] = wall.published

    unshare_form = UnshareForm(request.POST or None)
    if unshare_form.is_valid():
        email = request.POST['email']
        return HttpResponseRedirect('/walls/unshare/%s' % (wid, email))
    unshare_form.initial['unshared'] = True

#    publish_form = PublishWallForm(request.POST or None)
#    if publish_form.is_valid() and request.POST['published']:
#        published = request.POST['published']
#        messages.info(request, 'published: %s | %s | %s ' % (published,
#                                                             type(published), 
#                                                             len(published)))
#        messages.info(request, published)
#        wall.published.append(published)
#        messages.info(request, '%s added to published list on %s (%s)' % (published, wall.name, wall.id))
#        box = Box.objects.get(id=published)
#        box.walls.append(published)
#        box.save()
#        return HttpResponseRedirect('/walls/update/%s' % wid)

    update_form = UpdateWallForm(request.POST or None)
    if update_form.is_valid():
        wall.name = request.POST['name']  # update wall name
        # get latest email and add to walls.sharing if valid
        invited = request.POST['invited'] 
        real = User.objects.filter(email=invited)
        
        if real and invited not in wall.sharing:
            wall.sharing.append(invited)
        wall.save()

        # then update records and publish to selected appliances

        # update wall.published with appliance ids
        messages.info(request, 'invited: %s | %s | %s ' % (invited, 
                                                           type(invited), 
                                                           len(invited)))
        return HttpResponseRedirect('/walls/update/%s' % wid)

    update_form.initial['name'] = wall.name
    update_form.fields['name'].label = 'WikiWall Name'
    update_form.fields['invited'].label = 'Invite new users'
#    update_form.fields['published'].label = 'Publish your WikiWall to an appliance'


    # for box in wall.published:

    #boxes = [ Box.objects.get(box) for box in wall.published ]
    data = {'title': 'Kolabria - Edit Board Details', 
            'wall': wall,
            'owner': wall.owner.email,
            'sharing': wall.sharing,
#            'boxes' : boxes,
            'update_form': update_form,
            'unshare_form': unshare_form,
            'unpublish_form': unpublish_form,
            }

    return render_to_response('walls/update.html', data,
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
