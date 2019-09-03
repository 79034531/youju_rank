from django.urls import path
from . import views

app_name = 'rank'

urlpatterns = [
    path('', views.RankView.as_view(), name='rank'),
    path('boss/', views.BossView.as_view(), name='boss')
]
