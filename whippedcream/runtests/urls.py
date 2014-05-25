from django.conf.urls import patterns, url, include

from whippedcream.tests.urls import v1_api, noname_api


urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),
    url(r'^apinoname/', include(noname_api.urls))
)
