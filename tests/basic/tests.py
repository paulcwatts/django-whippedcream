from django.test import TestCase


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
