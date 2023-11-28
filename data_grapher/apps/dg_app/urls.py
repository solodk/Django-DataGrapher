from django.urls import path

from . import views

app_name = 'dg_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>', views.project, name='project'),
    path('projects/<int:project_id>/table/<int:table_id>', views.table, name='table'),
    path('projects/<int:project_id>/table/<int:table_id>/edit', views.edit_table, name='edit_table'),
    path('projects/<int:project_id>/table/create', views.create_table, name='create_table'),
]