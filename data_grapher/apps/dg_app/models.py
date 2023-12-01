from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Table(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.JSONField()

    def __str__(self):
        """
        Return a representation of entry in a string
        """
        return f"{self.name}"

class Graph(models.Model):

    GRAPH_TYPES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('hist', 'Histogram'),
        ('scatter', 'Scatter Plot'),
        ('area', 'Area Chart'),
        ('bubble', 'Bubble Chart'),
        ('box', 'Box-and-Whisker Plot'),
        ('radar', 'Radar Chart'),
        ('heatmap', 'Heatmap'),
        ('treemap', 'Treemap'),
        ('network', 'Network Graph'),
    ]

    name = models.CharField(max_length=128)
    graph_type = models.CharField(max_length=20, choices=GRAPH_TYPES)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    y_axis = models.IntegerField()
    x_axis = models.IntegerField()