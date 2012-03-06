from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

from kolabria.login import views
#from kolabria.walls.views import my_walls, view_wall

urlpatterns = patterns('',
    url(r'^login/$', 'views.mongo_login'),
    url(r'^loggedin/$', 'views.mongo_loggedin'),
    url(r'^logout/$', 'views.mongo_logout'),
    url(r'^register/$', 'views.mongo_register'),

    url(r'^walls/$', 'views.mongo_walls'),
    url(r'^walls/<id>$', 'view_wall'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^includes/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/home/alok/kolabria/kolabria/static/'}),
    ) 
