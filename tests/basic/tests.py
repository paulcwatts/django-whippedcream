import time
from datetime import datetime
from django.test import TestCase
from django.utils.unittest import skipUnless

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
