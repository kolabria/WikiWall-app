from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
 

from kolabria.login.forms import RegistrationForm

def registration(request):
    
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            
            login(request, user)
            
            return HttpResponseRedirect("/login")
    
    return render_to_response('login/registration.html', {'form' : form}, context_instance=RequestContext(request))

@login_required
def loggedin(request):
    # this is the redirect page for a logged in user 
    return render_to_response('login/loggedin.html', context_instance=RequestContext(request))
