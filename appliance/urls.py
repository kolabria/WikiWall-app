from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = patterns('',
    (r'^appliances/$', login_required(TemplateView.as_view(
                         template_name="appliance/myappliances.html"))),
#    (r'^details/(?P<box>\w+)/$', login_required(TemplateView.as_view()),
)

"""
urlpatterns = patterns('appliance',
    url(r'^register/(?P<box>\w+)/$', views.register),
    url(r'^edit/(?P<box>\w+)/$', views.edit),
    url(r'^remove/(?P<box>\w+)/$', views.remove),
    url(r'^$', views.appliances),
)

from django.conf import settings

import views 


urlpatterns += patterns('',
    url(r'^appliances/$', views.appliances),

    # these urls are for internal dev and debug purposes only
    url(r'^the-appliance/$', views.the_appliance),
    url(r'^id-appliance/$', views.id_appliance),
)
"""
