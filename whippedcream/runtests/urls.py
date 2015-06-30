import django
from whippedcream.tests.urls import v1_api, noname_api


if django.VERSION[0] == 1 and django.VERSION[1] >= 8:
    from django.conf.urls import url, include

    def patterns(_a, *args):
        return args
else:
    from django.conf.urls import patterns, url, include


urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),
    url(r'^apinoname/', include(noname_api.urls))
)
