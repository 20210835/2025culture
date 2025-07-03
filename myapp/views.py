# C:\Users\www45\myproject\myapp\views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Content, Hotel, Restaurant, Actor
from .utils import find_nearby_locations

def search_view(request):
    """
    미디어 콘텐츠를 검색하고 결과를 표시하는 뷰입니다.
    제목, 배우 이름, 주소_지역명으로 필터링할 수 있습니다.
    """
    query = request.GET.get('query', '')
    region = request.GET.get('region', '')
    
    # 디버그를 위한 print 문 추가 (이 부분이 중요합니다!)
    print(f"DEBUG: Received query: '{query}'")
    print(f"DEBUG: Received region: '{region}'")

    contents = Content.objects.all()
    print(f"DEBUG: Initial Content count: {contents.count()}") # 초기 콘텐츠 개수

    if query:
        # 제목 또는 배우 이름으로 검색
        contents = contents.filter(
            Q(title__icontains=query) | 
            Q(actors__name__icontains=query)
        ).distinct() # 중복 결과 제거
        print(f"DEBUG: Content count after query filter: {contents.count()}")

    if region:
        # 주소_지역명으로 필터링
        contents = contents.filter(address_region__icontains=region)
        print(f"DEBUG: Content count after region filter: {contents.count()}")

    # 모든 고유한 주소_지역명 목록을 가져와 필터링 옵션으로 제공
    all_regions = Content.objects.values_list('address_region', flat=True).distinct().exclude(address_region__isnull=True).exclude(address_region__exact='')
    print(f"DEBUG: All regions: {sorted(list(all_regions))}") # 모든 지역 목록 확인
    
    context = {
        'query': query,
        'region': region,
        'contents': contents,
        'all_regions': sorted(list(all_regions)), # 지역명 정렬
    }
    return render(request, 'myapp/search.html', context)


def map_view(request, content_id):
    """
    선택된 콘텐츠를 중심으로 주변 콘텐츠, 맛집, 호텔을 지도에 표시합니다.
    """
    selected_content = get_object_or_404(Content, id=content_id)

    base_lat = selected_content.latitude
    base_lon = selected_content.longitude

    if base_lat is None or base_lon is None:
        return render(request, 'myapp/map.html', {'error_message': '선택된 콘텐츠의 위치 정보가 없습니다.'})

    locations_for_map = []
    path_coordinates = []

    # 1. 선택된 콘텐츠 정보 추가
    locations_for_map.append({
        'id': selected_content.id,
        'name': selected_content.title,
        'type': '콘텐츠',
        'latitude': base_lat,
        'longitude': base_lon,
        'address': selected_content.address,
        'description': selected_content.place_description,
    })
    path_coordinates.append([base_lat, base_lon])

    # 2. 가까운 다른 콘텐츠 2개 찾기 (최대 10km 반경)
    nearby_contents = find_nearby_locations(
        base_lat, base_lon, Content,
        exclude_id=selected_content.id,
        limit=2,
        max_distance_km=10
    )
    for nc in nearby_contents:
        locations_for_map.append({
            'id': nc.id,
            'name': nc.title,
            'type': '콘텐츠',
            'latitude': nc.latitude,
            'longitude': nc.longitude,
            'address': nc.address,
            'description': nc.place_description,
        })
        path_coordinates.append([nc.latitude, nc.longitude])

    # 3. 각 콘텐츠 위치 기준으로 주변 맛집, 호텔 3개씩 찾기 (반경 5km)
    content_points = [loc for loc in locations_for_map if loc['type'] == '콘텐츠']

    for point in content_points:
        lat = point['latitude']
        lon = point['longitude']

        # 맛집
        nearby_restaurants = find_nearby_locations(lat, lon, Restaurant, limit=3, max_distance_km=5)
        for r in nearby_restaurants:
            locations_for_map.append({
                'id': r.id,
                'name': r.Name,  # 모델 필드명이 Name
                'type': '맛집',
                'latitude': r.latitude,
                'longitude': r.longitude,
                'address': r.Addr,  # 모델 필드명이 Addr
                'description': r.Category,  # 간단하게 카테고리 표시
            })

        # 호텔
        nearby_hotels = find_nearby_locations(lat, lon, Hotel, limit=3, max_distance_km=5)
        for h in nearby_hotels:
            locations_for_map.append({
                'id': h.id,
                'name': h.LDGS_NM,
                'type': '호텔',
                'latitude': h.latitude,
                'longitude': h.longitude,
                'address': h.LDGS_ADDR,
                'description': h.LDGMNT_TY_NM,  # 호텔 유형
            })

    context = {
        'selected_content': selected_content,
        'locations_json': locations_for_map,
        'path_coords_json': path_coordinates,
    }
    return render(request, 'myapp/map.html', context)
