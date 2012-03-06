from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

from django.contrib.auth import authenticate, logout, login

from mongoengine.django import auth
from mongoengine.django.auth import User

from kolabria.login.forms import LoginForm, RegistrationForm

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
        logout(request)
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
            user_name = request.POST['username']
            email = request.POST['email']
            pass_word = request.POST['password1']
            new_user = User.create_user(username=user_name, email=email,
                                        password=pass_word)
            new_user.save()
            auth_user = authenticate(username=user_name, password=pass_word)
            login(request=request, user=auth_user)
        #TODO FIX broken redirect on registration -- now points to
        # /register/register-success/
            return render_to_response('mongo/register-success.html',
                              context_instance=RequestContext(request))
