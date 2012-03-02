from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth import authenticate, logout, login

from mongoengine.django import auth
from mongoengine.django.auth import User

from kolabria.forms import LoginForm, RegistrationForm
from kolabria.models import Wall

def mongo_login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            login(request=request, user=user)            
            return render_to_response('mongo/loggedin.html',
                                      context_instance=RequestContext(request))
            return HttpResponseRedirect('loggedin/')
    data = {'title': 'Kolabria - Login Page',
            'form': form,}                        
    return render_to_response('mongo/login.html', data,
                              context_instance=RequestContext(request))

def mongo_loggedin(request):
    return render_to_response('mongo/loggedin.html',
                              context_instance=RequestContext(request))

def mongo_logout(request):
    if request.user.is_authenticated():
        logout()
    return HttpResponseRedirect('/mongo/login/')
        
def mongo_register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        data = {'title': 'Kolabria - Registration Page',
                'form': form,}
        return render_to_response('mongo/register.html', data,
                                  context_instance=RequestContext(request))
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            pass 
        return HttpResponseRedirect('mongo/register-success/')

def mongo_register_success(request):
    return render_to_response('mongo/register-success.html',
                              context_instance=RequestContext(request))


def mongo_walls(request):
    walls = Wall.objects.filter(owner=request.user)
    data = {'title': 'Kolabria - My Whiteboards',
            'walls': walls,}
    return render_to_response('mongo/mywalls.html', data,
                              context_instance=RequestContext(request))


