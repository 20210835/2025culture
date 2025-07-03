# Create your views here.
# myproject/myapp/views.py

# myproject/myapp/views.py

from django.shortcuts import render
from .models import Restaurant, Hotel # 모델 임포트 (다시 활성화)

def index(request):
    # 데이터베이스에서 모든 맛집 데이터 가져오기 (예: 별점 높은 순 10개)
    restaurants = Restaurant.objects.all().order_by('-Score')[:3]
    
    # 데이터베이스에서 모든 숙박 데이터 가져오기 (예: 평균 점수 높은 순 10개)
    hotels = Hotel.objects.all().order_by('-LDGS_AVRG_SCORE_CO')[:3]

    # 템플릿에 전달할 컨텍스트 (데이터)
    context = {
        'restaurants': restaurants,
        'hotels': hotels,
    }
    
    # 'index.html' 템플릿을 렌더링하면서 데이터 전달
    return render(request, 'index.html', context)

# 추가적으로 특정 맛집 상세 페이지를 위한 뷰 (선택 사항 - 필요 없으면 지워도 됩니다)
def restaurant_detail(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        from django.http import Http404
        raise Http404("Restaurant does not exist")
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})