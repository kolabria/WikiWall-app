from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^walls/$', views.walls),
    url(r'^walls/(?P<wid>\w+)/$', views.view_wall),

    url(r'^create-wall/$', views.create_wall),
    url(r'^config-wall/$', views.config_wall),
    url(r'^delete-wall/$', views.delete_wall),

    url(r'^idwall/$', views.idwall),
    url(r'^thewall/$', views.thewall),
    url(r'^modal/$', views.modal),
    url(r'^new-wall/$', views.new_wall),
)
