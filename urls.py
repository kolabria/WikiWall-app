from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^home/$', 'kolabria.home.views.index'),
    (r'^date/$', 'kolabria.home.views.date'),
#    (r'^time/$', 'tut.app.views.time'),
#    (r'^time/plus/(\d{1,2})/$', hours_ahead),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
