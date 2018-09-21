from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'home'

urlpatterns = [
    path('', IndexView, name='index'),
    path('search', search, name='search'),
    path('ordenaPlay/<str:pesquisa>', playordena, name='ordena_play_view'),
    path('ordenaAudio/<str:pesquisa>', audioordena, name='ordena_audio_view'),
    path('ordenaCanais/<str:pesquisa>', ordenaCanais, name='ordena_channel_view'),
    path('report/<int:audio_id>', login_required(report_audio), name='report_view'),
    path('visualized/', visualized, name='visualized_view')

]
