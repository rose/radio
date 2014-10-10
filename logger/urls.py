from django.conf.urls import include, url
from logger.views import *

urlpatterns = [
    url(r'^$', ListShowView.as_view(), name='shows'),
    url(r'^login$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^show/(?P<pk>\d+)$', EditShowView.as_view(), name='edit-show'),
    url(r'^episode/(?P<pk>\d+)$', EditEpisodeView.as_view(), name='edit-episode'),
]
