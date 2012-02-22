from django.conf.urls.defaults import include, patterns, url
import django.contrib.auth.views
from login import views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^index/$', 'kolabria.home.views.index'),
    url(r'^date/$', 'kolabria.home.views.date'),
    (r'^accounts/', include('kolabria.accounts.urls')),
    url(r'^login/$', django.contrib.auth.views.login, 
                    {'template_name': 'home.html'}, name = 'home'),
    url(r'^logout/$', django.contrib.auth.views.logout, 
                    {'template_name': 'logout.html'}),
    url(r'^register/$', views.registration),
   
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
