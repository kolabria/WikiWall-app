from django.conf.urls.defaults import include, patterns, url
import django.contrib.auth.views
from login import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^index/$', 'kolabria.home.views.index'),
    url(r'^date/$', 'kolabria.home.views.date'),

    url(r'^login/$', django.contrib.auth.views.login, 
                    {'template_name': 'login/home.html'}, name = 'home'),
    url(r'^logout/$', django.contrib.auth.views.logout, 
                    {'template_name': 'login/logout.html'}),
    url(r'^register/$', views.registration),
  
    url(r'^loggedin/$', views.loggedin),
 
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
#    (r'^accounts/', include('kolabria.accounts.urls')),
)
