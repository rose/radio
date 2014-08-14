from django.conf.urls import patterns, include, url

from ajax_select import urls as ajax_select_urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'radio.views.home', name='home'),
    url(r'^logger/', include('logger.urls'), name='logger'),
    url(r'^crazy/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
