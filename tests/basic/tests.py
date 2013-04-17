import time
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase
from django.utils.unittest import skipUnless

from resources import Name, NamesResource

try:
    import json as simplejson
except ImportError:  # < Python 2.6
    from django.utils import simplejson

try:
    import pytz
except ImportError:
    pytz = None


class SerializerTest(TestCase):
    def test_default(self):
        "The default format is JSON."
        response = self.client.get('/api/v1/names/')
        self.assertEqual('application/json', response['Content-Type'])

    def test_html(self):
        "Adding an accept field returns the Debug JSON"
        response = self.client.get('/api/v1/names/', HTTP_ACCEPT='text/html')
        self.assertEqual('text/html; charset=utf-8', response['Content-Type'])
        self.assertContains(response, 'Debug JSON')


class ViewAccessMixin(TestCase):
    def test_get_obj(self):
        req = HttpRequest()
        obj = Name(1, "Miles Davis")
        r = NamesResource()
        result = r.get_json(req, obj)
        EXPECTED = '{"id": 1, "name": "Miles Davis", "resource_uri": ""}'
        self.assertEqual(EXPECTED, result)

    def test_get_list(self):
        req = HttpRequest()
        obj1 = Name(1, "Miles Davis")
        obj2 = Name(2, "John Coltrane")
        r = NamesResource()
        result = r.get_json_list(req, [obj1, obj2])
        EXPECTED1 = '{"id": 1, "name": "Miles Davis", "resource_uri": ""}'
        EXPECTED2 = '{"id": 2, "name": "John Coltrane", "resource_uri": ""}'
        self.assertEqual("[" + EXPECTED1 + ", " + EXPECTED2 + "]", result)


@skipUnless(pytz, "This test requires pytz")
class DateTimeFieldTest(TestCase):
    def test_field(self):
        dt = datetime(year=2013, month=4, day=5,
                      hour=12, minute=24, second=30)
        # I know this is ugly, it's just for testing.
        ts = time.mktime(dt.timetuple())
        id = str(ts + 0.24601).replace('.', '_')
        response = self.client.get('/api/v1/dt/%s/' % id)
        # We should get JSON back
        self.assertEqual('application/json', response['Content-Type'])
        result = simplejson.loads(response.content)
        EXPECTED = {
            u'dt': u'2013-04-05T19:24:30',
            u'dt_normalized': u'2013-04-05T19:24:30',
            u'dt_default': u'2013-04-05T19:24:30.250000',
            u'dt_aware': u'2013-04-05T19:24:30+00:00',
            u'dt_aware_default': u'2013-04-05T19:24:30.250000+00:00',
            u'dt_aware_normalized': u'2013-04-05T19:24:30+00:00',
            u'resource_uri': u'',
        }
        self.assertEqual(result, EXPECTED)


class ApiTest(TestCase):
    def test_url_get(self):
        response = self.client.get('/apinoname/names/')
        self.assertEqual('application/json', response['Content-Type'])

    def test_top_level(self):
        response = self.client.get('/apinoname/')
        self.assertEqual('application/json', response['Content-Type'])

    def test_reverse(self):
        # This is able to reverse a URL
        url = reverse("api_dispatch_list",
                      kwargs={'api_name': '', 'resource_name': 'names'})
        self.assertEqual('/apinoname/names/', url)
