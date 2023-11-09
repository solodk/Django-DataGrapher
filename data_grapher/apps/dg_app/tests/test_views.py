from django.test import TestCase, Client
from django.urls import reverse

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('dg_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dg_app/index.html')