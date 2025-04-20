# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<str:username>/', views.chat_detail, name='chat_detail'),
]
