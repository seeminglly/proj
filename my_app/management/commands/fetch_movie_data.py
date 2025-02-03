import requests
from django.core.management.base import BaseCommand
from my_app.models import Movie
from datetime import datetime


class Command(BaseCommand):
    help = 'Fetches movie data from KOFIC API and saves it to the database'

    def handle(self, *args, **kwargs):
        api_key = '04c52266e1fdcfe2b96d62445a151a99'  # API 키를 여기에 입력하세요
        url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={api_key}&targetDt=20000101'
        response = requests.get(url)
        print(response.json())  # JSON 응답을 출력하여 확인\ㅂ
        
        data = response.json()

        movie_list = data.get('movieListResult', {}).get('movieList', [])

        for movie_data in movie_list:
            movie_cd = movie_data['movieCd']
            movie_nm = movie_data['movieNm']
            open_dt = movie_data['openDt']
            
            # 날짜 형식이 'YYYYMMDD' 형식이면, 이를 'YYYY-MM-DD' 형식으로 변환
            try:
                open_dt = datetime.strptime(open_dt, '%Y%m%d').date()  # 날짜 변환
            except ValueError:
                open_dt = None  # 잘못된 날짜 형식이 있으면 None 처리

            genre = movie_data.get('genre', None)  # 장르가 없을 수 있음
            director = movie_data.get('director', None)  # 감독이 없을 수 있음
            poster_url = movie_data.get('posterUrl', None)  # 포스터 URL이 없을 수 있음
            box_office_sales = movie_data.get('salesAmt', None)  # 매출
            box_office_rank = movie_data.get('rank', None)  # 순위

            # Movie 모델에 데이터 저장
            movie, created = Movie.objects.update_or_create(
                movie_cd=movie_cd,
                defaults={
                    'movie_nm': movie_nm,
                    'open_dt': open_dt,
                    'genre': genre,
                    'director': director,
                    'poster_url': poster_url,
                    'box_office_sales': box_office_sales,
                    'box_office_rank': box_office_rank,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"새로운 영화가 추가되었습니다: {movie_nm}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"영화 정보가 업데이트되었습니다: {movie_nm}"))
