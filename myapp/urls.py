# C:\Users\www45\myproject\myapp\urls.py

from django.urls import path
from . import views

app_name = 'myapp'  # 네임스페이스가 있으면 꼭 확인!

urlpatterns = [
    path('', views.search_view, name='home'),
    path('search/', views.search_view, name='search'),
]
