# C:\Users\www45\myproject\myapp\urls.py

from django.urls import path
from . import views

app_name = 'myapp' # 이 줄이 정확히 'myapp'으로 설정되어 있어야 합니다.

urlpatterns = [
    path('', views.search_view, name='search'), # 검색 페이지 (기본 경로)
    # 아래 'map_view' URL 패턴이 정확히 정의되어 있는지 확인해주세요.
    # <int:content_id>는 URL에서 정수형 content_id를 받아 map_view 함수로 전달합니다.
    path('map/<int:content_id>/', views.map_view, name='map_view'), # 지도 상세 페이지
]