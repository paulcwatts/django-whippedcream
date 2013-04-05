from tastypie.serializers import Serializer as BaseSerializer
from tastypie.utils import format_datetime, make_naive

from django.core.serializers import json
try:
    import json as simplejson
except ImportError:  # < Python 2.6
    from django.utils import simplejson


class Serializer(BaseSerializer):
    """
    This serializer implements the "html" format to display.

    It also allows you to pass aware-datetime objects through and
    have them serialized with a timezone value. Pass allow_aware_datetime=True
    to the constructor.
    """
    html_body = """<!DOCTYPE html>
<html>
<head></head>
<!-- We need the h1 to prevent JSONView from taking over -->
<body><h1>Debug JSON</h1><pre class="json">%s</pre></body>
</html>"""

    def __init__(self, *args, **kwargs):
        self.allow_aware_datetime = kwargs.pop('allow_aware_datetime', False)
        super(Serializer, self).__init__(*args, **kwargs)

    def format_datetime(self, data):
        """
        A hook to control how datetimes are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "2010-12-16T03:02:14".
        """
        if not self.allow_aware_datetime:
            data = make_naive(data)
        if self.datetime_formatting == 'rfc-2822':
            return format_datetime(data)

        return data.isoformat()

    def to_html(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        jsontext = simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                                    indent=4, sort_keys=True)
        return self.html_body % jsontext
