from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'radio.views.home', name='home'),
    url(r'^logger/', include('logger.urls'), name='logger'),
    url(r'^admin/', include(admin.site.urls)),
)
