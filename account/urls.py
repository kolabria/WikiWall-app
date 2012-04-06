from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^(?P<company>\w+)/welcome/$', views.welcome),
)
