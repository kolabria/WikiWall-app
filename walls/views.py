from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from kolabria.walls.models import Wall

@login_required
def mywalls(request):
    walls = Wall.objects.filter(owner=request.user.id)
    return render_to_response('walls/mywalls.html', {
        'title': 'Kolabria - My Whiteboards',
        'walls': walls,
    },
    context_instance=RequestContext(request))
         
