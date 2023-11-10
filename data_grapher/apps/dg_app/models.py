from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Table(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.JSONField()

    def __str__(self):
        """
        Return a representation of entry in a string
        """
        return f"{self.project.owner.username}'s {self.project.name} table"