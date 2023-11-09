from django.test import TestCase, Client
from django.urls import reverse

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
    
    def test_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertTemplateUsed(response, 'registration/login.html')