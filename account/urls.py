from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^(?P<company>\w+)/welcome/$', views.welcome),
    url(r'^(?P<company>\w+)/admin/$', views.welcome),
    url(r'^(?P<company>\w+)/admin/appliance/add/$', views.add_box),
    url(r'^(?P<company>\w+)/admin/appliance/update/(?P<bid>\w+)/$', views.update_box),
#    url(r'^(?P<company>\w+)/admin/appliance/delete/$', views.del_box),
)
