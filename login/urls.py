from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.views import login
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^$', views.public),
    url(r'^public/$', views.public),
    url(r'^login/$', views.login_user),
    url(r'^loggedin/$', views.loggedin),
    url(r'^logout/$', views.logout_user),
    url(r'^register/$', views.register),
    
#    url(r'^knock/$', login, {'template': '),
)
