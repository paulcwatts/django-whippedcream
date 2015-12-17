import time
import json
import six
from six import BytesIO
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase
try:
    from unittest import skipUnless
except ImportError:
    from django.utils.unittest import skipUnless

from .resources import Name, NamesResource

try:
    import pytz
except ImportError:
    pytz = None


class ViewAccessMixin(TestCase):
    def test_get_obj(self):
        req = HttpRequest()
        obj = Name(1, "Miles Davis")
        r = NamesResource()
        result = json.dumps(r.obj_to_simple(req, obj), sort_keys=True)
        EXPECTED = '{"id": 1, "name": "Miles Davis", "resource_uri": ""}'
        self.assertEqual(EXPECTED, result)

    def test_get_list(self):
        req = HttpRequest()
        obj1 = Name(1, "Miles Davis")
        obj2 = Name(2, "John Coltrane")
        r = NamesResource()
        result = json.dumps(r.list_to_simple(req, [obj1, obj2]), sort_keys=True)
        META = '"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 2}'
        EXPECTED1 = '{"id": 1, "name": "Miles Davis", "resource_uri": ""}'
        EXPECTED2 = '{"id": 2, "name": "John Coltrane", "resource_uri": ""}'
        self.assertEqual('{{{}, "objects": [{}, {}]}}'.format(META, EXPECTED1, EXPECTED2), result)


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
        result = json.loads(response.content.decode('utf-8'))
        ms = "250000" if six.PY2 else "246010"
        EXPECTED = {
            u'dt': u'2013-04-05T19:24:30',
            u'dt_normalized': u'2013-04-05T19:24:30',
            u'dt_default': u'2013-04-05T19:24:30.' + ms,
            u'dt_aware': u'2013-04-05T19:24:30+00:00',
            u'dt_aware_default': u'2013-04-05T19:24:30.{0}+00:00'.format(ms),
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


class FileUploadTest(TestCase):
    def test_upload(self):
        fileobj = BytesIO(b"This is my file.")
        fileobj.name = "hello.txt"
        response = self.client.post('/api/v1/file/', {'myfile': fileobj})
        self.assertEqual(201, response.status_code)
        self.assertEqual('application/json', response['Content-Type'])
        content = json.loads(response.content.decode('utf-8'))
        self.assertIn('resource_uri', content)

        # Now we should be able to get this file?
        response = self.client.get(content['resource_uri'])
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response['Content-Type'])
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual('hello.txt', content['myfile'])

    def test_absfile(self):
        fileobj = BytesIO(b"This is my absolute file.")
        fileobj.name = "hello2.txt"
        response = self.client.post('/api/v1/file/', {'myabsfile': fileobj})
        self.assertEqual(201, response.status_code)
        self.assertEqual('application/json', response['Content-Type'])
        content = json.loads(response.content.decode('utf-8'))
        self.assertIn('resource_uri', content)
        self.assertTrue(content['myabsfile'].startswith("http://"))
