from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', IndexView, name='index'),
    path('search', search, name='search'),
    path('ordenaPlay/<str:pesquisa>', playordena, name='ordena_play_view'),
    path('ordenaAudio/<str:pesquisa>', audioordena, name='ordena_audio_view'),
    path('ordenaCanais/<str:pesquisa>', ordenaCanais, name='ordena_channel_view')

]
