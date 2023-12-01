from django.contrib import admin

from .models import Project, Table, Graph

admin.site.register(Project)
admin.site.register(Table)
admin.site.register(Graph)