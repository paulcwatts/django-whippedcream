from django.conf.urls import patterns, url, include

from basic.urls import v1_api


urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls))
)
