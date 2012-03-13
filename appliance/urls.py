from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('appliance',
    url(r'^detail/(?P<box>\w+)/$', views.detail), 
    url(r'^register/(?P<box>\w+)/$', views.register),
    url(r'^edit/(?P<box>\w+)/$', views.edit),
    url(r'^remove/(?P<box>\w+)/$', views.remove),
    url(r'^$', views.appliances),
)

urlpatterns += patterns('',
    url(r'^appliances/$', views.appliances),

    # these urls are for internal dev and debug purposes only
    url(r'^the-appliance/$', views.the_appliance),
    url(r'^id-appliance/$', views.id_appliance),
)
