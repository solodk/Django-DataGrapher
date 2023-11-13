from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.dg_app.models import Project, Table

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.table_data = {'key': 'value'}

        self.user = User.objects.create(
            username='test_user', 
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='test_project',
            owner=self.user
        )
        self.table = Table.objects.create(
            project=self.project,
            content=self.table_data,
            name='test_table'
        )

    def test_index_view(self):
        response = self.client.get(reverse('dg_app:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dg_app/index.html')
    
    def test_logged_homepage_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dg_app:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="/projects/">Projects</a>')
        self.assertContains(response, '<a>Templates</a>')
        self.assertContains(response, '<p>{Latest Templates}</p>')

    def test_unlogged_homepage_view(self):
        self.client.logout()
        response = self.client.get(reverse('dg_app:home'))

        # Check if the response status code 
        # 200 (OK) or 302 (redirect to login page)
        self.assertIn(response.status_code, [200, 302])

        # Check if the content for unauthenticated users is present
        if response.status_code == 302:
            expected_url = reverse('accounts:login') + '?next=' + reverse('dg_app:home')
            self.assertRedirects(response, expected_url)
        else:
            self.assertContains(
                response, 
                '<p>You need to be logged in to see this page</p>'
            )