# C:\Users\www45\myproject\myapp\views.py

# from django.shortcuts import render
# from geopy.distance import geodesic
# from .models import Drama, Movie, Singer, Restaurant, Hotel

# def search_view(request):
#     if request.method == 'POST':
#         media_type = request.POST.get('media_type', '').strip().lower()
#         name = request.POST.get('name', '').strip()
#         region = request.POST.get('region', '').strip()

#         # media_type에 따라 QuerySet 생성
#         if media_type == 'drama':
#             qs = Drama.objects.filter(
#                 actors__name__icontains=name,
#                 address_region__iexact=region
#             ).distinct()
#         elif media_type == 'movie':
#             qs = Movie.objects.filter(
#                 actors__name__icontains=name,
#                 address_region__iexact=region
#             ).distinct()
#         elif media_type == 'artist':
#             qs = Singer.objects.filter(
#                 artists__name__icontains=name,
#                 address_region__iexact=region
#             ).distinct()
#         else:
#             return render(request, 'myapp/search.html', {'error': 'media_type은 drama, movie, artist 중 하나여야 합니다.'})

#         if not qs.exists():
#             return render(request, 'myapp/search.html', {'error': '해당 배우/아티스트와 지역 조합으로 데이터가 없습니다.'})

#         # 장소타입별 최대 3개씩 가져오기
#         place_types = qs.values_list('place_type', flat=True).distinct()
#         recommend_place = []
#         for pt in place_types:
#             places = qs.filter(place_type=pt)[:3]
#             recommend_place.extend(places)

#         selected_place = recommend_place[0]
#         place_lat = selected_place.latitude
#         place_lng = selected_place.longitude

#         def calc_distance_to_place(obj):
#             try:
#                 return geodesic((place_lat, place_lng), (obj.latitude, obj.longitude)).meters
#             except:
#                 return float('inf')

#         restaurants = Restaurant.objects.filter(
#             Area=region,
#             Category__iexact='restaurant'
#         )
#         cafes = Restaurant.objects.filter(
#             Area=region,
#             Category__iexact='cafe'
#         )
#         hotels = Hotel.objects.filter(
#             LDGS_ADDR=region
#         )

#         rest_list = [{
#             'name': r.Name,
#             'distance': calc_distance_to_place(r),
#             'score': r.Score,
#             'review_num': r.Review_Num,
#             'addr': r.Addr,
#             'link': r.Link,
#         } for r in restaurants]

#         cafe_list = [{
#             'name': c.Name,
#             'distance': calc_distance_to_place(c),
#             'score': c.Score,
#             'review_num': c.Review_Num,
#             'addr': c.Addr,
#             'link': c.Link,
#         } for c in cafes]

#         hotel_list = [{
#             'name': h.LDGS_NM,
#             'distance': calc_distance_to_place(h),
#             'grade': h.LDGS_GRAD_VALUE,
#             'min_price': h.LDGS_MIN_PRC,
#             'max_price': h.LDGS_MXMM_PRC,
#             'score': h.LDGS_AVRG_SCORE_CO,
#             'addr': h.LDGS_ROAD_NM_ADDR,
#         } for h in hotels]

#         rest_list = sorted(rest_list, key=lambda x: x['distance'])[:3]
#         cafe_list = sorted(cafe_list, key=lambda x: x['distance'])[:3]
#         hotel_list = sorted(hotel_list, key=lambda x: x['distance'])[:3]

#         context = {
#             'place_title': getattr(selected_place, 'title', ''),
#             'place_name': selected_place.place_name,
#             'place_type': selected_place.place_type,
#             'restaurants': rest_list,
#             'cafes': cafe_list,
#             'hotels': hotel_list,
#         }
#         return render(request, 'myapp/map.html', context)

#     return render(request, 'myapp/search.html')

# C:\Users\www45\myproject\myapp\views.py

from django.shortcuts import render
from geopy.distance import geodesic
from .models import Drama, Movie, Singer, Restaurant, Hotel
import folium # folium import 추가
import pandas as pd # pandas import 추가 (데이터프레임 처리용)

# myapp/utils.py에 calc_distance가 있다면 이 함수를 사용하도록 수정 권장
# from .utils import calc_distance

def search_view(request):
    if request.method == 'POST':
        media_type = request.POST.get('media_type', '').strip().lower()
        name = request.POST.get('name', '').strip()
        region = request.POST.get('region', '').strip()

        # media_type에 따라 QuerySet 생성
        if media_type == 'drama':
            qs = Drama.objects.filter(
                actors__name__icontains=name,
                address_region__iexact=region
            ).distinct()
        elif media_type == 'movie':
            qs = Movie.objects.filter(
                actors__name__icontains=name,
                address_region__iexact=region
            ).distinct()
        elif media_type == 'artist':
            qs = Singer.objects.filter(
                artists__name__icontains=name,
                address_region__iexact=region
            ).distinct()
        else:
            return render(request, 'myapp/search.html', {'error': 'media_type은 drama, movie, artist 중 하나여야 합니다.'})

        if not qs.exists():
            return render(request, 'myapp/search.html', {'error': '해당 배우/아티스트와 지역 조합으로 데이터가 없습니다.'})

        # 장소타입별 최대 3개씩 가져오기
        place_types = qs.values_list('place_type', flat=True).distinct()
        recommend_place_objects = [] # ORM 객체 리스트
        for pt in place_types:
            places = qs.filter(place_type=pt)[:3]
            recommend_place_objects.extend(places)
        
        # VS Code 스크립트처럼 첫 번째 촬영지를 선택하는 로직 유지
        selected_place = recommend_place_objects[0]
        place_lat = selected_place.latitude
        place_lng = selected_place.longitude

        # calc_distance_to_place 함수 정의 (utils.py의 calc_distance 활용 권장)
        def calc_distance_to_place(obj):
            try:
                # 여기서 obj.latitude, obj.longitude가 None이 아닌지 확인하는 로직 추가하면 더 안전
                if obj.latitude is None or obj.longitude is None:
                    return float('inf')
                return geodesic((place_lat, place_lng), (obj.latitude, obj.longitude)).meters
                # return calc_distance(place_lat, place_lng, obj.latitude, obj.longitude) # utils 함수 사용 시
            except Exception:
                return float('inf')

        restaurants_qs = Restaurant.objects.filter(
            Area__iexact=region, # 이전에 논의된 icontains나 정확한 지역명 사용 고려
            Category__iexact='restaurant'
        )
        cafes_qs = Restaurant.objects.filter(
            Area__iexact=region, # 이전에 논의된 icontains나 정확한 지역명 사용 고려
            Category__iexact='cafe'
        )
        hotels_qs = Hotel.objects.filter(
            LDGS_ADDR__iexact=region # 이전에 논의된 icontains나 정확한 지역명 사용 고려
        )

        # 리스트 컴프리헨션으로 데이터와 거리 계산 (None 체크 추가)
        rest_list = []
        for r in restaurants_qs:
            if r.latitude is not None and r.longitude is not None:
                rest_list.append({
                    'name': r.Name,
                    'distance': calc_distance_to_place(r),
                    'score': r.Score,
                    'review_num': r.Review_Num,
                    'addr': r.Addr,
                    'link': r.Link,
                    'latitude': r.latitude, # 지도에 표시하기 위해 추가
                    'longitude': r.longitude, # 지도에 표시하기 위해 추가
                })
        
        cafe_list = []
        for c in cafes_qs:
            if c.latitude is not None and c.longitude is not None:
                cafe_list.append({
                    'name': c.Name,
                    'distance': calc_distance_to_place(c),
                    'score': c.Score,
                    'review_num': c.Review_Num,
                    'addr': c.Addr,
                    'link': c.Link,
                    'latitude': c.latitude, # 지도에 표시하기 위해 추가
                    'longitude': c.longitude, # 지도에 표시하기 위해 추가
                })

        hotel_list = []
        for h in hotels_qs:
            if h.latitude is not None and h.longitude is not None:
                hotel_list.append({
                    'name': h.LDGS_NM,
                    'distance': calc_distance_to_place(h),
                    'grade': h.LDGS_GRAD_VALUE,
                    'min_price': h.LDGS_MIN_PRC,
                    'max_price': h.LDGS_MXMM_PRC,
                    'score': h.LDGS_AVRG_SCORE_CO,
                    'addr': h.LDGS_ROAD_NM_ADDR,
                    'latitude': h.latitude, # 지도에 표시하기 위해 추가
                    'longitude': h.longitude, # 지도에 표시하기 위해 추가
                })


        rest_list = sorted(rest_list, key=lambda x: x['distance'])[:3]
        cafe_list = sorted(cafe_list, key=lambda x: x['distance'])[:3]
        hotel_list = sorted(hotel_list, key=lambda x: x['distance'])[:3]

        # ---------------------- Folium 지도 생성 부분 추가 ----------------------
        # 중심 좌표 설정 (선택된 촬영지)
        map_center = [place_lat, place_lng] if place_lat is not None and place_lng is not None else [37.5665, 126.9780] # 기본 서울 좌표

        m = folium.Map(location=map_center, zoom_start=12)

        # 🎬 촬영지 마커 (선택된 단일 촬영지)
        if selected_place.latitude is not None and selected_place.longitude is not None:
            popup_html = f"""
                <b>{getattr(selected_place, 'title', '제목 없음')}</b><br>
                장소명: {selected_place.place_name}<br>
                장소타입: {selected_place.place_type}<br>
                설명: {getattr(selected_place, 'place_description', '-')}<br>
                주소: {getattr(selected_place, 'address', '-')}
            """
            folium.Marker(
                [selected_place.latitude, selected_place.longitude],
                popup=folium.Popup(folium.Html(popup_html, script=True), max_width=300),
                icon=folium.Icon(icon='video-camera', prefix='fa', color='blue')
            ).add_to(m)

        # 🍽 맛집/카페 마커
        for item in rest_list + cafe_list:
            if item['latitude'] is not None and item['longitude'] is not None:
                # `item` 딕셔너리에 'link' 키가 없는 경우를 대비하여 .get() 사용
                website = item.get('link', '')
                if not pd.isna(website) and not str(website).startswith("http"):
                    website = "https://" + str(website)

                html = f"""
                    <b>{item.get('name', '이름 없음')}</b><br>
                    카테고리: {item.get('category', '-')}<br>
                    별점: {item.get('score', '-')}<br>
                    리뷰수: {item.get('review_num', '-')}<br>
                    주소: {item.get('addr', '-')}<br>
                    <a href="{website}" target="_blank">웹사이트</a>
                """
                folium.Marker(
                    [item['latitude'], item['longitude']],
                    popup=folium.Popup(folium.Html(html, script=True), max_width=300),
                    icon=folium.Icon(icon='cutlery', prefix='fa', color='red')
                ).add_to(m)

        # 🏨 숙박 마커
        for item in hotel_list:
            if item['latitude'] is not None and item['longitude'] is not None:
                popup_html = f"""
                    <b>{item.get('name', '이름 없음')}</b><br>
                    도로명 주소: {item.get('addr', '-')}<br>
                    성급: {item.get('grade', '-')}<br>
                    최소가격: {item.get('min_price', '-') if item.get('min_price') is not None else '-'}원<br>
                    최대가격: {item.get('max_price', '-') if item.get('max_price') is not None else '-'}원<br>
                    평균평점: {item.get('score', '-')}
                """
                folium.Marker(
                    [item['latitude'], item['longitude']],
                    popup=folium.Popup(folium.Html(popup_html, script=True), max_width=300),
                    icon=folium.Icon(icon='bed', prefix='fa', color='green')
                ).add_to(m)
        
        # 지도를 HTML 문자열로 변환하여 템플릿에 전달
        map_html = m._repr_html_()

        context = {
            'place_title': getattr(selected_place, 'title', ''),
            'place_name': selected_place.place_name,
            'place_type': selected_place.place_type,
            'restaurants': rest_list,
            'cafes': cafe_list,
            'hotels': hotel_list,
            'map_html': map_html, # 지도 HTML 추가
        }
        return render(request, 'myapp/map.html', context)

    return render(request, 'myapp/search.html')