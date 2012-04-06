from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kolabria.appliance.forms import NewBoxForm, UpdateBoxForm, DelBoxForm
from kolabria.account.models import Account
from kolabria.appliance.models import Box
from mongoengine.django.auth import User

import ipdb

@login_required
def welcome(request, company):
    account = Account.objects.get(name__iexact=company)
    boxes = Box.objects.filter(company=account)

    if request.user.username == account.admin.username:
        messages.success(request, 'You are the authorized admin for account')
    else:
        messages.warning(request, 'You are not the authorized admin for account')
        return HttpResponseRedirect('/')

    new_box_form = NewBoxForm(request.POST or None)
    update_box_form = UpdateBoxForm()
    del_box_form = DelBoxForm()
    if new_box_form.is_valid():
        name = request.POST['name']
        location = request.POST['location']
        new_box = Box.objects.create(company=account,
                                     owner=request.user,
                                     name=name,
                                     location=location)
        new_box.save()
        msg = 'Added new appliance name: %s  location: %s' % (name, location)
        messages.success(request, msg)
        return HttpResponseRedirect('/%s/admin/' % company)

    data = {'title': 'Kolabria - New Account Landing',
            'company': company,
            'boxes': boxes,
            'new_box_form': new_box_form,
            'update_box_form': update_box_form,
            'del_box_form': del_box_form, }
    return render_to_response('account/welcome.html', data,
                              context_instance=RequestContext(request))


@login_required
def add_box(request, company):
    account = Account.objects.get(name__iexact=company)
    form = NewBoxForm(request.POST or None)
    if form.is_valid():
        name = request.POST['name']
        location = request.POST['location']
        status = request.POST['status']
        box = Box.objects.create(company=account,
                                 owner=account.admin,
                                 name=name,
                                 location=location,
                                 status=status)
        box.save()
        messages.success(request, 'Created box %s %s' % (box.name, box.location))
        return HttpResponseRedirect('/%s/admin/' % company)

    data = {'title': 'Kolabria - Add New Appliance',
            'company': company,
            'form': form, }

    return render_to_response('appliance/create.html', data,
                              context_instance=RequestContext(request))

@login_required
def update_box(request, company, bid):
    account = Account.objects.get(name__iexact=company)
    box = Box.objects.get(id=bid)
    form = UpdateBoxForm(request.POST or None)
    if form.is_valid():
        box.company = account
        box.owner = account.admin
        box.name = request.POST['name']
        box.location = request.POST['location']
        box.status = request.POST['status']
        box.save()
        messages.success(request, 'Updated box %s %s' % (box.name, box.location))
        return HttpResponseRedirect('/%s/admin/' % company)

    form.initial['name'] = box.name
    form.initial['location'] = box.location
    form.initial['status'] = box.status
    data = {'title': 'Kolabria - Update Appliance Details',
            'box': box,
            'company': company,
            'form': form, }
    return render_to_response('appliance/update.html', data,
                              context_instance=RequestContext(request))



@login_required
def admin(request, company):
#    account = Account.objects.filter(name=company)[0]
#    if request.user is not account.admin:
#        messages.warning(request, 'You are not authorized to access admin')
#        return HttpResponseRedirect('/')
    new_box_form = NewBoxForm(request.POST or None)
    update_box_form = UpdateBoxForm()
    del_box_form = DelBoxForm()
    if new_box_form.is_valid():
        name = request.POST['name']
        location = request.POST['location']
        new_box = Box.objects.create
    data = {'title': 'Kolabria - New Account Landing',
            'company': company,
            'new_box_form': new_box_form,
            'update_box_form': update_box_form,
            'del_box_form': del_box_form, }
    return render_to_response('account/welcome.html', data,
                              context_instance=RequestContext(request))


"""
    account = Account.objects.filter(name=company)[0]
    if account and request.user is not account.admin:
        messages.warning(request, '%s not authorized to administer %s' % \
                                            (request.user.username, company))
        return HttpResponseRedirect('/')
    else:
        form = NewBoxForm(request.POST or None)
        if form.is_valid():
            name = request.POST['name']
            location = request.POST['location']
            box = Box.objects.create(name=name, location=location)
            box.save()
            msg = '%s %s %s' % (box.id, box.name, box.location)
            messages.info(request, msg)
            messages.info(request, request.POST)
            return HttpResponseRedirect('/%s /welcome/' % company)
"""

