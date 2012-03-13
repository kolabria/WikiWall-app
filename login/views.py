from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from mongoengine.django import auth
from mongoengine.django.auth import User

from kolabria.login.forms import LoginForm, RegistrationForm
from kolabria.walls.models import Wall

def public(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/walls')
    else:
        return HttpResponseRedirect('/login')

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/walls')
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            login(request=request, user=user)            
            return HttpResponseRedirect('/walls')
    
    data = {'title': 'Kolabria - Login Page',
            'form': form,}
    return render_to_response('login/login.html', data,
                              context_instance=RequestContext(request))

@login_required
def loggedin(request):
    return render_to_response('login/loggedin.html',
                              context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')

def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        data = {'title': 'Kolabria - Registration Page',
                'form': form,}
        return render_to_response('login/register.html', data,
                                  context_instance=RequestContext(request))
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = request.POST['username']
            email = request.POST['email']
            pass_word = request.POST['password1']
            new_user = User.create_user(username=user_name, email=email,
                                        password=pass_word)
            new_user.save()
            auth_user = authenticate(username=user_name, password=pass_word)
            login(request=request, user=auth_user)
            return render_to_response('login/register-success.html',
                              context_instance=RequestContext(request))
