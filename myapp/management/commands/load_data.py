# myproject/myapp/management/commands/load_data.py

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
# 모델들을 임포트합니다. 'myapp'은 여러분의 앱 이름이어야 합니다.
from myapp.models import Restaurant, Hotel

class Command(BaseCommand):
    help = 'Loads restaurant and hotel data from CSVs into the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data loading process...'))

        # --- 1. 맛집 데이터 로딩 (Restaurant) ---
        restaurant_csv_path = r'C:\Users\www45\Desktop\문화\(중복제거)kakao_food_geocode.csv'
        self.stdout.write(f'Loading restaurant data from: {restaurant_csv_path}')

        try:
            df_restaurants = pd.read_csv(restaurant_csv_path)
        except FileNotFoundError:
            raise CommandError(f'Restaurant CSV file not found at: {restaurant_csv_path}')
        except Exception as e:
            raise CommandError(f'Error reading restaurant CSV: {e}')

        self.stdout.write(self.style.WARNING('Deleting existing restaurant data...'))
        Restaurant.objects.all().delete() # 기존 데이터 삭제

        restaurant_count = 0
        for index, row in df_restaurants.iterrows():
            try:
                # Score, latitude, longitude는 부동소수점이며 NaN 값이 올 수 있으므로 처리
                score = row['별점'] if pd.notna(row['별점']) else None
                latitude = row['위도'] if pd.notna(row['위도']) else None
                longitude = row['경도'] if pd.notna(row['경도']) else None

                Restaurant.objects.create(
                    Name=row['식당이름'],
                    Category=row['카테고리'],
                    Score=score,
                    Review_Num=row['리뷰 수'],
                    Link=row['웹사이트'],
                    Addr=row['주소'],
                    Area=row['지역명'],
                    latitude=latitude,
                    longitude=longitude,
                )
                restaurant_count += 1
            except KeyError as e:
                self.stderr.write(self.style.ERROR(f"Skipping restaurant row {index}: Missing column '{e}'. Check CSV headers."))
                continue # 해당 열이 없으면 건너뛰고 다음 행 처리
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Skipping restaurant row {index}: Error creating Restaurant object: {e} - Data: {row.to_dict()}"))
                continue # 오류 발생 시 건너뛰고 다음 행 처리

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {restaurant_count} restaurant entries.'))


        # --- 2. 숙박 데이터 로딩 (Hotel) ---
        hotel_csv_path = r'C:\Users\www45\Desktop\문화\hotel_address.csv'
        self.stdout.write(f'Loading hotel data from: {hotel_csv_path}')

        try:
            df_hotels = pd.read_csv(hotel_csv_path)
        except FileNotFoundError:
            raise CommandError(f'Hotel CSV file not found at: {hotel_csv_path}')
        except Exception as e:
            raise CommandError(f'Error reading hotel CSV: {e}')

        self.stdout.write(self.style.WARNING('Deleting existing hotel data...'))
        Hotel.objects.all().delete() # 기존 데이터 삭제

        hotel_count = 0
        for index, row in df_hotels.iterrows():
            try:
                # Hotel 모델 필드에 맞춰 NaN 값 처리
                ldgs_grad_value = row['LDGS_GRAD_VALUE'] if pd.notna(row['LDGS_GRAD_VALUE']) else None
                ldgmt_ty_nm = row['LDGMNT_TY_NM'] if pd.notna(row['LDGMNT_TY_NM']) else None
                ldgs_avrg_prc = row['LDGS_AVRG_PRC'] if pd.notna(row['LDGS_AVRG_PRC']) else None
                ldgs_min_prc = row['LDGS_MIN_PRC'] if pd.notna(row['LDGS_MIN_PRC']) else None
                ldgs_mxmm_prc = row['LDGS_MXMM_PRC'] if pd.notna(row['LDGS_MXMM_PRC']) else None
                ldgs_avrg_score_co = row['LDGS_AVRG_SCORE_CO'] if pd.notna(row['LDGS_AVRG_SCORE_CO']) else None
                hotel_latitude = row['위도'] if pd.notna(row['위도']) else None
                hotel_longitude = row['경도'] if pd.notna(row['경도']) else None

                Hotel.objects.create(
                    LDGS_NM=row['LDGS_NM'],
                    LDGS_ADDR=row['LDGS_ADDR'],
                    LDGS_ROAD_NM_ADDR=row['LDGS_ROAD_NM_ADDR'],
                    GSRM_SCALE_CN=row['GSRM_SCALE_CN'],
                    LDGS_GRAD_VALUE=ldgs_grad_value,
                    LDGMNT_TY_NM=ldgmt_ty_nm,
                    LDGS_AVRG_PRC=ldgs_avrg_prc,
                    LDGS_MIN_PRC=ldgs_min_prc,
                    LDGS_MXMM_PRC=ldgs_mxmm_prc,
                    LDGS_AVRG_SCORE_CO=ldgs_avrg_score_co,
                    latitude=hotel_latitude,
                    longitude=hotel_longitude,
                )
                hotel_count += 1
            except KeyError as e:
                self.stderr.write(self.style.ERROR(f"Skipping hotel row {index}: Missing column '{e}'. Check CSV headers."))
                continue
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Skipping hotel row {index}: Error creating Hotel object: {e} - Data: {row.to_dict()}"))
                continue

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {hotel_count} hotel entries.'))
        self.stdout.write(self.style.SUCCESS('Data loading process completed.'))


# 촬영지
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from myapp.models import Content, Actor 

class Command(BaseCommand):
    help = 'CSV 파일을 읽어 데이터베이스에 Content와 Actor 데이터를 로드합니다.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='로드할 CSV 파일의 경로')

    def handle(self, *args, **options):
        csv_file_path = csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'파일을 찾을 수 없습니다: {csv_file_path}')

        self.stdout.write(self.style.SUCCESS(f'CSV 파일 "{csv_file_path}" 로드를 시작합니다...'))

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # CSV 파일의 헤더와 모델 필드 매핑
            # CSV 파일의 헤더: 미디어타입	제목	장소명	장소타입	장소설명	주소	위도	경도	주소_지역명	배우이름
            # 모델 필드: media_type, title, place_name, place_type, place_description, address, latitude, longitude, address_region, actors
            
            for row in reader:
                # 위도, 경도 값 처리 (빈 문자열이거나 숫자가 아닐 경우 None 처리)
                try:
                    latitude = float(row.get('위도')) if row.get('위도') else None
                except ValueError:
                    latitude = None

                try:
                    longitude = float(row.get('경도')) if row.get('경도') else None
                except ValueError:
                    longitude = None

                # Content 객체 생성 또는 업데이트 (제목, 장소명 조합으로 고유성 가정)
                content, created = Content.objects.update_or_create(
                    title=row['제목'],
                    place_name=row['장소명'],
                    defaults={
                        'media_type': row.get('미디어타입', ''),
                        'place_type': row.get('장소타입'),
                        'place_description': row.get('장소설명'),
                        'address': row.get('주소'),
                        'latitude': latitude,
                        'longitude': longitude,
                        'address_region': row.get('주소_지역명'),
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'새 Content 생성: {content.title} - {content.place_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Content 업데이트: {content.title} - {content.place_name}'))

                # 배우 이름 처리
                actor_names_str = row.get('배우이름', '')
                if actor_names_str:
                    # 배우 이름이 "[배우1, 배우2]" 형태로 되어 있다면 파싱 (실제 CSV 포맷 확인 필요)
                    # 만약 그냥 "배우1, 배우2" 형태라면 split(',') 만 사용
                    # 여기서는 "[배우1, 배우2]" 형태를 가정하고 파싱
                    try:
                        # 파이썬 리스트 문자열을 실제 리스트로 변환
                        # eval 사용은 보안상 위험할 수 있으나, 신뢰할 수 있는 CSV 파일에만 사용
                        # 더 안전한 방법은 ast.literal_eval 사용
                        import ast
                        actor_list = ast.literal_eval(actor_names_str)
                    except (ValueError, SyntaxError):
                        # 리스트 형태가 아니라면 콤마로 분리 시도 (예: "배우1, 배우2")
                        actor_list = [name.strip() for name in actor_names_str.split(',') if name.strip()]
                    
                    if not isinstance(actor_list, list): # 여전히 리스트가 아니면 단일 항목으로 처리
                        actor_list = [actor_names_str.strip()]
                    
                    for actor_name in actor_list:
                        if actor_name: # 빈 이름은 건너뛰기
                            actor, _ = Actor.objects.get_or_create(name=actor_name.strip())
                            content.actors.add(actor)
                
        self.stdout.write(self.style.SUCCESS('CSV 파일 로드 완료!'))