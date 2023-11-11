from django.urls import path

from . import views

app_name = 'dg_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
]