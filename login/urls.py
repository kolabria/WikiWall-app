from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^public/$', views.public),
    url(r'^login/$', views.login_user),
    url(r'^loggedin/$', views.loggedin),
    url(r'^logout/$', views.logout_user),
    url(r'^register/$', views.register),
)
