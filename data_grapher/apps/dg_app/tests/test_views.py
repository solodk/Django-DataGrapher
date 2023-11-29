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