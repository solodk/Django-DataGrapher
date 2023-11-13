from django.test import TestCase
from apps.dg_app.models import Project, Table
from django.contrib.auth.models import User


class ModelTests(TestCase):
    def setUp(self):
        self.table_data = {'key': 'value'}

        self.user = User.objects.create(
            username="Test_user", 
            password="test_password"
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

    def test_table_str(self):
        self.assertEqual(str(self.table), self.table.name)
    
    def test_table_project_connection(self):
        db_table = Table.objects.get(id=self.table.id)
        self.assertEqual(db_table.project, self.project)
    
    def test_table_content(self):
        db_table = Table.objects.get(id=self.table.id)
        self.assertEqual(db_table.content, self.table_data)

    def test_table_date_added(self):
        db_table = Table.objects.get(id=self.table.id)
        self.assertIsNotNone(db_table.date_created)