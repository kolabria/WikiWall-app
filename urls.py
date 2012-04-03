from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

urlpatterns = patterns('',
    (r'', include('account.urls')),
    (r'', include('login.urls')),
    (r'', include('walls.urls')),
    (r'', include('users.urls')),
    (r'', include('appliance.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^includes/(?P<path>.*)$', 'django.views.static.serve',
    #TODO: generalize static serve doc root
         {'document_root': '/home/alok/kolabria/kolabria/static/'}),
    )
