from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^walls/$', views.walls),
    url(r'^walls/create/$', views.create_wall),
    url(r'^walls/modal/$', views.modal),
    url(r'^walls/share/(?P<wid>\w+)/$', views.share_wall),
    url(r'^walls/unshare/(?P<wid>\w+)/$', views.unshare_wall),
    url(r'^walls/unpublish/(?P<wid>\w+)/$', views.unpublish_wall),
    url(r'^walls/update/(?P<wid>\w+)/$', views.update_wall),
    url(r'^walls/delete/(?P<wid>\w+)/$', views.delete_wall),
#    url(r'^walls/unshare/?P<wid>[\d]+)/$', views.unshare),
    url(r'^walls/(?P<wid>\w+)/$', views.view_wall),
    url(r'^idwall/$', views.idwall),
    url(r'^thewall/$', views.thewall),
)
