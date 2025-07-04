import csv
import os
import ast
import pandas as pd
from django.core.management.base import BaseCommand
from myapp.models import (
    Restaurant, Hotel,
    Movie, Drama, Singer,
    Actor, Artist
)

class Command(BaseCommand):
    help = '모든 CSV 데이터를 한 번에 불러와서 DB에 로드합니다.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('✅ 데이터 로드 시작'))

        self.load_restaurant_data()
        self.load_hotel_data()
        self.load_movie_data()
        self.load_drama_data()
        self.load_singer_data()

        self.stdout.write(self.style.SUCCESS('✅ 모든 데이터 로드 완료!'))


    ### 1️⃣ 맛집
    def load_restaurant_data(self):
        csv_path = r'C:\Users\www45\Desktop\문화\(중복제거)kakao_food_geocode.csv'
        self.stdout.write(f'🍴 [맛집] CSV: {csv_path}')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING('⚠️ 맛집 CSV가 존재하지 않습니다.'))
            return

        df = pd.read_csv(csv_path)
        Restaurant.objects.all().delete()

        for _, row in df.iterrows():
            try:
                Restaurant.objects.create(
                    Name=row['식당이름'],
                    Category=row['카테고리'],
                    Score=row['별점'] if pd.notna(row['별점']) else None,
                    Review_Num=row['리뷰 수'],
                    Link=row['웹사이트'],
                    Addr=row['주소'],
                    Area=row['지역명'],
                    latitude=row['위도'] if pd.notna(row['위도']) else None,
                    longitude=row['경도'] if pd.notna(row['경도']) else None,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ 맛집 스킵: {e}"))
        self.stdout.write(self.style.SUCCESS('✅ 맛집 데이터 완료'))


    ### 2️⃣ 호텔
    def load_hotel_data(self):
        csv_path = r"C:\Users\www45\Desktop\문화\hotel_pre.csv"
        self.stdout.write(f'🏨 [호텔] CSV: {csv_path}')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING('⚠️ 호텔 CSV가 존재하지 않습니다.'))
            return

        df = pd.read_csv(csv_path)
        Hotel.objects.all().delete()

        for _, row in df.iterrows():
            try:
                Hotel.objects.create(
                    LDGS_NM=row['LDGS_NM'],
                    LDGS_ADDR=row['LDGS_ADDR'],
                    LDGS_ROAD_NM_ADDR=row['LDGS_ROAD_NM_ADDR'],
                    GSRM_SCALE_CN=row['GSRM_SCALE_CN'],
                    LDGS_GRAD_VALUE=row['LDGS_GRAD_VALUE'] if pd.notna(row['LDGS_GRAD_VALUE']) else None,
                    LDGMNT_TY_NM=row['LDGMNT_TY_NM'] if pd.notna(row['LDGMNT_TY_NM']) else None,
                    LDGS_MIN_PRC=row['LDGS_MIN_PRC'] if pd.notna(row['LDGS_MIN_PRC']) else None,
                    LDGS_MXMM_PRC=row['LDGS_MXMM_PRC'] if pd.notna(row['LDGS_MXMM_PRC']) else None,
                    LDGS_AVRG_SCORE_CO=row['LDGS_AVRG_SCORE_CO'] if pd.notna(row['LDGS_AVRG_SCORE_CO']) else None,
                    latitude=row['위도'] if pd.notna(row['위도']) else None,
                    longitude=row['경도'] if pd.notna(row['경도']) else None,
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ 호텔 스킵: {e}"))
        self.stdout.write(self.style.SUCCESS('✅ 호텔 데이터 완료'))


import csv
import os
import ast
from django.core.management.base import BaseCommand, CommandError
from myapp.models import Movie, Drama, Singer, Actor, Artist

def parse_names_list(names_str):
    if not names_str:
        return []

    try:
        val = ast.literal_eval(names_str)
        if isinstance(val, list):
            return [str(name).strip() for name in val if str(name).strip()]
    except (ValueError, SyntaxError):
        pass

    return [name.strip() for name in names_str.split(',') if name.strip()]

class Command(BaseCommand):
    help = '기존 데이터 삭제 후 Movie, Drama, Singer CSV 파일을 모두 읽어 데이터베이스에 추가/수정합니다.'

    def float_or_none(self, val):
        try:
            return float(val) if val else None
        except ValueError:
            return None

    def clear_all_data(self):
        self.stdout.write(self.style.WARNING('기존 데이터 삭제 중...'))
        Movie.objects.all().delete()
        Drama.objects.all().delete()
        Singer.objects.all().delete()
        Actor.objects.all().delete()
        Artist.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('기존 모든 미디어 및 관련 배우/아티스트 데이터 삭제 완료!'))

    def load_movies(self, csv_path):
        self.stdout.write(self.style.SUCCESS(f'Movie CSV "{csv_path}" 로드 시작...'))
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                latitude = self.float_or_none(row.get('위도'))
                longitude = self.float_or_none(row.get('경도'))

                movie = Movie.objects.create(
                    title=row['제목'],
                    place_name=row['장소명'],
                    media_type=row.get('미디어타입', ''),
                    place_type=row.get('장소타입'),
                    place_description=row.get('장소설명'),
                    address=row.get('주소'),
                    latitude=latitude,
                    longitude=longitude,
                    address_region=row.get('주소_지역명'),
                )

                actor_list = parse_names_list(row.get('배우이름', ''))
                for actor_name in actor_list:
                    actor, _ = Actor.objects.get_or_create(name=actor_name)
                    movie.actors.add(actor)

                self.stdout.write(self.style.SUCCESS(f'Movie 생성: {movie.title}'))

        self.stdout.write(self.style.SUCCESS('Movie CSV 로드 완료!'))

    def load_dramas(self, csv_path):
        self.stdout.write(self.style.SUCCESS(f'Drama CSV "{csv_path}" 로드 시작...'))
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                latitude = self.float_or_none(row.get('위도'))
                longitude = self.float_or_none(row.get('경도'))

                drama = Drama.objects.create(
                    title=row['제목'],
                    place_name=row['장소명'],
                    media_type=row.get('미디어타입', ''),
                    place_type=row.get('장소타입'),
                    place_description=row.get('장소설명'),
                    address=row.get('주소'),
                    latitude=latitude,
                    longitude=longitude,
                    address_region=row.get('주소_지역명'),
                )

                actor_list = parse_names_list(row.get('배우이름', ''))
                for actor_name in actor_list:
                    actor, _ = Actor.objects.get_or_create(name=actor_name)
                    drama.actors.add(actor)

                self.stdout.write(self.style.SUCCESS(f'Drama 생성: {drama.title}'))

        self.stdout.write(self.style.SUCCESS('Drama CSV 로드 완료!'))

    def load_singers(self, csv_path):
        self.stdout.write(self.style.SUCCESS(f'Singer CSV "{csv_path}" 로드 시작...'))
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                latitude = self.float_or_none(row.get('위도'))
                longitude = self.float_or_none(row.get('경도'))

                singer = Singer.objects.create(
                    title=row['제목'],
                    place_name=row['장소명'],
                    media_type=row.get('미디어타입', ''),
                    place_type=row.get('장소타입'),
                    place_description=row.get('장소설명'),
                    address=row.get('주소'),
                    latitude=latitude,
                    longitude=longitude,
                    address_region=row.get('주소_지역명'),
                )

                artist_list = parse_names_list(row.get('아티스트명', ''))
                for artist_name in artist_list:
                    artist, _ = Artist.objects.get_or_create(name=artist_name)
                    singer.artists.add(artist)

                self.stdout.write(self.style.SUCCESS(f'Singer 생성: {singer.title}'))

        self.stdout.write(self.style.SUCCESS('Singer CSV 로드 완료!'))

    def handle(self, *args, **options):
        movie_csv = "C:/Users/www45/Downloads/media_movie_pre.csv"
        drama_csv = "C:/Users/www45/Downloads/media_drama_pre.csv"
        singer_csv = "C:/Users/www45/Downloads/media_artist_pre.csv"

        if not (os.path.exists(movie_csv) and os.path.exists(drama_csv) and os.path.exists(singer_csv)):
            raise CommandError("CSV 파일 경로 중 하나 이상이 존재하지 않습니다.")

        self.clear_all_data()

        self.load_movies(movie_csv)
        self.load_dramas(drama_csv)
        self.load_singers(singer_csv)

        self.stdout.write(self.style.SUCCESS('기존 데이터 삭제 후 모든 미디어 데이터 로드 완료!'))

