from tastypie.serializers import Serializer as BaseSerializer

from django.core.serializers import json
try:
    import json as simplejson
except ImportError: # < Python 2.6
    from django.utils import simplejson


class Serializer(BaseSerializer):
    """
    This serializer implements the "html" format to display
    """
    html_body = """<!DOCTYPE html>
<html>
<head></head>
<!-- We need the h1 to prevent JSONView from taking over -->
<body><h1>Debug JSON</h1><pre class="json">%s</pre></body>
</html>"""

    def to_html(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        jsontext = simplejson.dumps(data, cls=json.DjangoJSONEncoder, indent=4, sort_keys=True)
        return self.html_body % jsontext
