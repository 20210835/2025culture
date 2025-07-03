# apps/utils.py
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    두 위도/경도 지점 간의 거리를 킬로미터(km) 단위로 계산합니다. (하버사인 공식)
    인자:
        lat1, lon1: 첫 번째 지점의 위도, 경도
        lat2, lon2: 두 번째 지점의 위도, 경도
    반환:
        두 지점 간의 거리 (km)
    """
    R = 6371  # 지구의 평균 반지름 (킬로미터)

    # 위도와 경도를 라디안으로 변환
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # 위도와 경도 차이
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # 하버사인 공식
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def find_nearby_locations(target_lat, target_lon, model, exclude_id=None, limit=3, max_distance_km=5):
    """
    주어진 위도/경도 주변에서 특정 모델의 가까운 객체들을 찾습니다.
    인자:
        target_lat, target_lon: 기준 지점의 위도, 경도
        model: 검색할 Django 모델 (예: Content, Hotel, Restaurant)
        exclude_id: 검색 결과에서 제외할 객체의 ID (선택 사항)
        limit: 반환할 최대 객체 수
        max_distance_km: 최대 검색 거리 (킬로미터)
    반환:
        거리순으로 정렬된 가까운 객체들의 리스트
    """
    nearby_objects = []
    
    # 위도, 경도 값이 유효한 객체만 필터링
    qs = model.objects.filter(latitude__isnull=False, longitude__isnull=False)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)

    for obj in qs:
        distance = haversine_distance(target_lat, target_lon, obj.latitude, obj.longitude)
        if distance <= max_distance_km:
            nearby_objects.append({'obj': obj, 'distance': distance})
    
    # 거리에 따라 정렬하고 제한된 수만큼 반환
    nearby_objects.sort(key=lambda x: x['distance'])
    return [item['obj'] for item in nearby_objects[:limit]]