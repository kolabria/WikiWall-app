from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.forms import NewWallForm, UpdateWallForm, DeleteWallForm
from kolabria.walls.forms import ShareWallForm, UnshareWallForm
from kolabria.walls.forms import PubWallForm, UnpubWallForm 

from mongoengine.django.auth import User
from kolabria.walls.models import Wall
from kolabria.appliance.models import Box

# Legend of urls and views
#walls             url(r'^walls/$', views.walls), 
#create            url(r'^walls/create/$', views.create_wall),
#view              url(r'^walls/share/(?P<wid>\w+)/$', views.share_wall),
#update_sharing    #
#share             url(r'^walls/unpublish/(?P<wid>\w+)/$', views.unshare_wall),
#unshare           url(r'^walls/unshare/(?P<wid>\w+)/$', views.unshare_wall),
#update            url(r'^walls/update/(?P<wid>\w+)/$', views.update_wall),
#delete_wall       url(r'^walls/delete/(?P<wid>\w+)/$', views.delete_wall),


@login_required
def create(request):
    form = NewWallForm(request.POST or None)
    form.fields['name'].label = 'Enter WikiWall Name'
    form.fields['invited'].label = 'Invite users by email'

    if form.is_valid():
        wall = Wall.objects.create(owner=request.user,
                                   name=request.POST['name'])
        wall.save()
        wid = wall.id
        name = wall.name

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
                except ObjectDoesNotExist:
                    messages.warning(request, 'Error: no account found for %s. Not invited')
                messages.info(request, 'Successfully added: %s' % email)


        if request.POST.getlist('publish'):
            # update wall.published model
            wall.published = request.POST.getlist('publish')
            wall.save()
            pub_msg = 'wall.published: %s' % wall.published
            messages.success(request, pub_msg)
            boxes = [ Box.objects.get(id=box) for box in wall.published ]
            messages.info(request, 'Boxes: %s' % boxes)
            for box in boxes:
                box_msg = 'box.name: %s | box.walls: %s | ' % (box.name, box.walls)
                box_msg += 'wall.name: %s | wall.id: %s' %  (wall.name,
                        wall.id)
                messages.info(request, box_msg)
                box.walls.append(str(wall.id))
                box.save()
                box_pub_msg = 'updated box.published to: %s for box.name: %s' % \
                                                            (box.walls, box.name)

        messages.success(request, 'Successfully created Wall: %s - %s' % \
                                                              (wid, name))
        return HttpResponseRedirect('/walls/create/')

    data = {'title': 'Kolabria - Create a new WikiWall',
            'form': form }
    return render_to_response('walls/create.html', data,
                              context_instance=RequestContext(request))


@login_required
def delete(request, wid):
    del_wall = Wall.objects.get(id=wid)
    del_form = DeleteWallForm(request.POST or None)
    del_form.fields['confirmed'].label = 'Confirm WikiWall Deletion'
    
    if del_form.is_valid():
        confirmed = request.POST.get('confirmed')
        del_wall_name = del_wall.name
        del_wall.delete()
        messages.info(request, 'Test Confirmed: Confirmed=%s for Wall Name: %s' % \
                                                            (confirmed, del_wall_name))
        messages.success(request, 'Successfully deleted WikiWall - %s' % del_wall_name)
        return HttpResponseRedirect('/walls/')
    
    data = {'title': 'Kolabria - Delete Board Confirmation',
            'del_wall': del_wall,
            'del_form': del_form,}
    return render_to_response('walls/delete.html', data,
                              context_instance=RequestContext(request))


@login_required
def publish(request, wid):
    pub_wall = Wall.objects.get(id=wid)
    pub_form = PubWallForm(request.POST or None)

    if  pub_form.is_valid():
        messages.info(request, 'original published: %s' % pub_wall.published )
#        publish = request.POST['publish']
#        pub_wall.published = publish
        messages.info(request, 'updated published: %s'  % publish)
#        pub_wall.save()
        return HttpResponseRedirect('/walls/update/%s' % wid)

    messages.error(request, 'error: no valid POST data found')
    return HttpResponseRedirect('/walls/update/%s' % wid)

#TODO Fix box updating logic, update > link on template to view that will
#     process POST request
#        boxes = Box.objects.filter(id=published)
#        box.walls.append(published)
#        box.save()



@login_required
def walls(request):
    # Generate New Wall Form logic but hide form behind modal
    new_form = NewWallForm()
    new_form.fields['name'].label = 'Enter WikiWall Name'
    invited_label = 'Invite users by email address separate by commas.'
    new_form.fields['invited'].label = invited_label

    del_form = DeleteWallForm()
    del_form.fields['confirmed'].label = ''
    del_form.initial['confirmed'] = True

    own = Wall.objects.filter(owner=request.user)
    shared = Wall.objects.filter(sharing=request.user.email)
    walls = {'own': own, 'shared': shared,}

    data = {'title': 'Kolabria - WikiWall Dashboard', 
            'walls': walls, 
            'new_form': new_form,
            'del_form': del_form, }

    return render_to_response('walls/mywalls.html', data,
                              context_instance=RequestContext(request))

@login_required
def view(request, wid):
    # Get a specific wall by Mongo object id
    wall = Wall.objects.get(id=wid)
    data = {'title': 'Kolabria - Viewing Wall %s' % wall.name,
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
def share(request, wid):
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
def unpublish(request, wid):
    wall = Wall.objects.get(id=wid)
    unpub_form = UnpubWallForm(request.POST or None)
   
    if unpub_form.is_valid():
        box_id = request.POST['box_id']
        if box_id in wall.published:
           wall.published.remove(box_id)
           wall.save()
           wall_unpub_msg = 'Wall Updated Successfully - wall.name: %s unpublished from '
           wall_unpub_msg += 'box.name: %s' % (wall.name, box.name)
           messages.success(request, wall_unpub_msg)
        wall_unpub_error_msg = 'Error wall.name: %s does not have access to box.name: %s.' % (wall.name, box.name)
        messages.warning(request, wall_unpub_error_msg)
        
        box = Box.objects.get(id=box_id)
        if box_id in box.walls:
            box.walls.remove(box_id)
            box.save()

            box_unpub_msg = 'Box Updated Successfully - wall.name: %s removed '
            box_unpub_msg += 'from box.published for %s' % (wall.name, box.name)
            box.success(request, box_unpub_msg)
        box_unpub_error_msg = 'Error box.name: %s does not have access to wall.name: %s.' % (box.name, wall.name)
        messages.warning(request, box_unpub_error_msg)

        return HttpResponseRedirect('/walls/update/%s' % wid)

    data = {'title': 'Kolabria - Unshare Wall with user',
            'wid': wid,
            'unpub_form': unpub_form, 
            'wall': wall,
            }
    return render_to_response('walls/update.html', data,
                              context_instance=RequestContext(request))



@login_required
def unshare(request, wid):
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
def update(request, wid):
    wall = Wall.objects.get(id=wid)
    boxids = wall.published
    boxes = [ Box.objects.get(id=str(boxid)) for boxid in boxids ]
        
    unpublish_form = UnpubWallForm()
    unpublish_form.initial['published'] = wall.published

    unshare_form = UnshareWallForm()
    unshare_form.initial['unshared'] = True

    pub_form = PubWallForm()
    pub_form.fields['publish'].label = 'Available Appliances'
    pub_form.initial['publish'] = wall.published

    unpub_form = UnpubWallForm({'unpublish': True })

    update_form = UpdateWallForm(request.POST or None)
    update_form.initial['name'] = wall.name
    update_form.fields['name'].label = 'Update WikiWall Name'
    update_form.fields['invited'].label = 'Invite new users by email address'

    if update_form.is_valid():
        wall.name = request.POST['name']  # update wall name
        invited = request.POST['invited'] 
        real = User.objects.filter(email=invited)
        
        if real and invited not in wall.sharing:
            wall.sharing.append(invited)
            messages.info(request, 'invited: %s' % invited)
        else:
            messages.warning(request, 'Error: %s not valid or already invited.' % invited)
        wall.save()

       # then update records and publish to selected appliances
       # update wall.published with appliance ids
        return HttpResponseRedirect('/walls/update/%s' % wid)

    data = {'title': 'Kolabria - Edit Board Details', 
            'wall': wall,
            'boxes': boxes,
            'pub_form': pub_form,
            'update_form': update_form,
            'unshare_form': unshare_form,
            'unpub_form': unpub_form, }

    return render_to_response('walls/update.html', data,
                              context_instance=RequestContext(request))
