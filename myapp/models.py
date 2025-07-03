from django.db import models

# Create your models here.

# 맛집 데이터 데이터베이스에 저장

class Restaurant(models.Model):
    Name = models.CharField(max_length=255)
    Category = models.CharField(max_length=255)
    Score = models.FloatField(null=True, blank=True)
    Review_Num = models.IntegerField()
    Link = models.URLField(max_length=500)
    Addr = models.CharField(max_length=500)
    Area = models.CharField(max_length=500)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.Name


# 숙박 데이터 데이터베이스에 저장

class Hotel(models.Model):
    LDGS_NM = models.CharField(max_length=255)
    LDGS_ADDR = models.CharField(max_length=255)
    LDGS_ROAD_NM_ADDR = models.CharField(max_length=255)
    GSRM_SCALE_CN = models.CharField(max_length=255)
    LDGS_GRAD_VALUE = models.CharField(max_length=255)
    LDGMNT_TY_NM = models.CharField(max_length=255)
    LDGS_AVRG_PRC = models.FloatField(null=True, blank=True)
    LDGS_MIN_PRC = models.FloatField(null=True, blank=True)
    LDGS_MXMM_PRC = models.FloatField(null=True, blank=True)
    LDGS_AVRG_SCORE_CO = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.LDGS_NM
    
       # apps/models.py

from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    media_type = models.CharField(max_length=100, verbose_name="미디어타입")
    title = models.CharField(max_length=255, verbose_name="제목")
    place_name = models.CharField(max_length=255, verbose_name="장소명")
    place_type = models.CharField(max_length=100, verbose_name="장소타입", null=True, blank=True)
    place_description = models.TextField(verbose_name="장소설명", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="주소", null=True, blank=True)
    latitude = models.FloatField(verbose_name="위도", null=True, blank=True)
    longitude = models.FloatField(verbose_name="경도", null=True, blank=True)
    address_region = models.CharField(max_length=100, verbose_name="주소_지역명", null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='contents', verbose_name="배우이름")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "콘텐츠"
        verbose_name_plural = "콘텐츠 목록"