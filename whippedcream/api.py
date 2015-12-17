import warnings

from django.conf.urls import include, url
from tastypie.api import Api as BaseApi
from tastypie.utils import trailing_slash
from .serializer import Serializer


class Api(BaseApi):
    """
    A version of the Api that doesn't require a name.
    It also uses the whippedcream serializer by default.
    """
    def __init__(self, serializer_class=Serializer):
        super(Api, self).__init__('', serializer_class)

    @property
    def urls(self):
        """
        Provides URLconf details for the ``Api`` and all registered
        ``Resources`` beneath it.
        """
        if self.api_name:
            api_pattern = '(?P<api_name>%s)'
            top_level = r"^%s%s$" % (api_pattern, trailing_slash())
        else:
            api_pattern = '(?P<api_name>)'
            top_level = r"^$"

        pattern_list = [
            url(top_level, self.wrap_view('top_level'), name="api_%s_top_level" % self.api_name),
        ]

        for name in sorted(self._registry.keys()):
            self._registry[name].api_name = self.api_name
            pattern_list.append(url(r"^%s" % api_pattern, include(self._registry[name].urls)))

        urlpatterns = self.prepend_urls()

        overridden_urls = self.override_urls()
        if overridden_urls:
            warnings.warn("'override_urls' is a deprecated method & will be removed by v1.0.0. Please rename your method to ``prepend_urls``.")
            urlpatterns += overridden_urls

        urlpatterns += pattern_list
        return urlpatterns
