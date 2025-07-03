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