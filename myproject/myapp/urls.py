from django.urls import path
from . import views # views.py에서 뷰 함수를 가져옵니다.

urlpatterns = [
    path('', views.index, name='index'), # 기본 경로에 views.index 함수 연결
    # path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'), # 상세 페이지 뷰 (필요 시 주석 해제)
]