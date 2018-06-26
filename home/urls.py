from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('search', views.search, name='search')
]