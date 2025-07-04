# C:\Users\www45\myproject\myapp\models.py
from django.db import models

# Create your models here.

# 맛집 데이터 데이터베이스에 저장

class Restaurant(models.Model):
    Name = models.CharField(max_length=255, verbose_name = '식당이름')
    Category = models.CharField(max_length=255, verbose_name = '카테고리')
    Score = models.FloatField(null=True, blank=True, verbose_name = '별점')
    Review_Num = models.IntegerField(verbose_name = '리뷰 수')
    Link = models.URLField(max_length=500, verbose_name = '웹사이트')
    Addr = models.CharField(max_length=500, verbose_name = '주소')
    Area = models.CharField(max_length=500, verbose_name = '지역명')
    latitude = models.FloatField(null=True, blank=True, verbose_name = '위도')
    longitude = models.FloatField(null=True, blank=True, verbose_name = '경도')
    
    def __str__(self):
        return self.Name


# 숙박 데이터 데이터베이스에 저장

class Hotel(models.Model):
    LDGS_NM = models.CharField(max_length=255, verbose_name = "숙박명")
    LDGS_ADDR = models.CharField(max_length=255, verbose_name = '지역명')
    LDGS_ROAD_NM_ADDR = models.CharField(max_length=255, verbose_name = '도로명주소')
    GSRM_SCALE_CN = models.CharField(max_length=255, verbose_name = '규모')
    LDGS_GRAD_VALUE = models.CharField(max_length=255, verbose_name = '성급')
    LDGMNT_TY_NM = models.CharField(max_length=255, verbose_name = '숙박유형')
    LDGS_MIN_PRC = models.FloatField(null=True, blank=True, verbose_name = '최소가격')
    LDGS_MXMM_PRC = models.FloatField(null=True, blank=True, verbose_name = '최대가격')
    LDGS_AVRG_SCORE_CO = models.FloatField(null=True, blank=True, verbose_name = '평균평점')
    latitude = models.FloatField(null=True, blank=True, verbose_name = '위도')
    longitude = models.FloatField(null=True, blank=True, verbose_name = '경도')
    
    def __str__(self):
        return self.LDGS_NM
    
       # apps/models.py


from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    media_type = models.CharField(max_length=100, verbose_name="미디어타입")
    title = models.CharField(max_length=255, verbose_name="제목")
    place_name = models.CharField(max_length=255, verbose_name="장소명")
    place_type = models.CharField(max_length=100, verbose_name="장소타입", null=True, blank=True)
    place_description = models.TextField(verbose_name="장소설명", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="주소", null=True, blank=True)
    latitude = models.FloatField(verbose_name="위도", null=True, blank=True)
    longitude = models.FloatField(verbose_name="경도", null=True, blank=True)
    address_region = models.CharField(max_length=100, verbose_name="주소_지역명", null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='MoActors', verbose_name='영화배우 이름')

class Drama(models.Model):
    media_type = models.CharField(max_length=100, verbose_name="미디어타입")
    title = models.CharField(max_length=255, verbose_name="제목")
    place_name = models.CharField(max_length=255, verbose_name="장소명")
    place_type = models.CharField(max_length=100, verbose_name="장소타입", null=True, blank=True)
    place_description = models.TextField(verbose_name="장소설명", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="주소", null=True, blank=True)
    latitude = models.FloatField(verbose_name="위도", null=True, blank=True)
    longitude = models.FloatField(verbose_name="경도", null=True, blank=True)
    address_region = models.CharField(max_length=100, verbose_name="주소_지역명", null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='DrActors', verbose_name= '드라마배우 이름')

class Singer(models.Model):
    media_type = models.CharField(max_length=100, verbose_name="미디어타입")
    title = models.CharField(max_length=255, verbose_name="제목")
    place_name = models.CharField(max_length=255, verbose_name="장소명")
    place_type = models.CharField(max_length=100, verbose_name="장소타입", null=True, blank=True)
    place_description = models.TextField(verbose_name="장소설명", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="주소", null=True, blank=True)
    latitude = models.FloatField(verbose_name="위도", null=True, blank=True)
    longitude = models.FloatField(verbose_name="경도", null=True, blank=True)
    address_region = models.CharField(max_length=100, verbose_name="주소_지역명", null=True, blank=True)
    artists = models.ManyToManyField(Artist, related_name='아티스트명')
