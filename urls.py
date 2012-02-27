from django.conf.urls.defaults import include, patterns, url
from django.conf import settings
import django.contrib.auth.views
from kolabria import home
from kolabria import login
from kolabria import walls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^index/$', 'home.views.index'),
    url(r'^date/$', 'home.views.date'),

    url(r'^login/$', django.contrib.auth.views.login, 
                    {'template_name': 'login/login.html'}, name = 'home'),
    url(r'^public/$', django.contrib.auth.views.login, 
                    {'template_name': 'boot/publichome.html'}, name = 'home'),
    url(r'^logout/$', django.contrib.auth.views.logout, 
                    {'template_name': 'login/logout.html'}),
    url(r'^register/$', 'login.views.registration'),
    url(r'^loggedin/$', 'login.views.loggedin'),
    url(r'^mywalls/$', 'walls.views.mywalls'),
)

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^includes/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/home/alok/kolabria/kolabria/static/'}),
    ) 
