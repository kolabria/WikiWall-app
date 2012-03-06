from django.conf.urls.defaults import include, patterns, url
from django.conf import settings
from kolabria import views

urlpatterns = patterns('',
    url(r'^login/$', 'views.mongo_login'),
    url(r'^loggedin/$', 'views.mongo_loggedin'),
    url(r'^logout/$', 'views.mongo_logout'),
    url(r'^register/$', 'views.mongo_register'),

    url(r'^walls/$', 'views.mongo_walls'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^includes/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/home/alok/kolabria/kolabria/static/'}),
    ) 
