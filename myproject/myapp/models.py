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
    
 