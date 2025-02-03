from django.db import models
from datetime import datetime




# 배우 모델
class Actor(models.Model):
    name = models.CharField(max_length=255)  # 배우 이름
    birth_date = models.DateField(null=True, blank=True)  # 생년월일 (선택 사항)

    def __str__(self):
        return self.name

# 영화 모델
class Movie(models.Model):
    movie_cd = models.CharField(max_length=20, unique=True)
    movie_nm = models.CharField(max_length=255)
    open_dt = models.CharField(max_length=10, null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    box_office_sales = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    box_office_rank = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField()  # 순위
    audi_cnt = models.IntegerField(default=0)  # 당일 관객수
    audi_acc = models.IntegerField(default=0)  # 누적 관객수

    def __str__(self):
        return self.movie_nm

class TVShow(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    vote_average = models.FloatField()
    popularity = models.FloatField()

    def __str__(self):
        return self.title