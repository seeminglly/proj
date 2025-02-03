# Create your views here.
from django.shortcuts import render
import requests
from django.http import JsonResponse
from bs4 import BeautifulSoup
from my_app.models import Movie, TVShow
from datetime import datetime, timedelta


def trending_tv_shows(request):
    api_key = 'bf5c5094ad11fd8f27152d30f1980757'
    url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}&language=ko-KR"
    
    # 어제 날짜로 설정
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

    # API 요청 파라미터
    params = {
        'key': api_key,
        'targetDt': yesterday,  # 날짜를 동적으로 변경
    }

    # TMDb API에서 트렌딩 TV 시리즈 정보 가져오기
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        trending_tv_data = response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        trending_tv_data = []
        print(f"API 요청 실패: {e}")
    
    # 데이터베이스에서 TV 시리즈 정보를 가져옵니다.
    tv_shows = TVShow.objects.all().order_by('popularity')

    # 포스터 이미지 URL 앞에 붙일 기본 URL
    image_base_url = 'https://image.tmdb.org/t/p/w500'
    
    # 트렌딩 TV 시리즈에 포스터 URL 추가하기
    for show in trending_tv_data:
        if show.get('poster_path'):
            show['poster_url'] = image_base_url + show['poster_path']
        else:
            show['poster_url'] = None  # 포스터가 없는 경우 처리

    # 템플릿으로 데이터 전달
    return render(request, 'my_app/trending_tv.html', {'tv_shows': trending_tv_data, 'database_tv_shows': tv_shows})
# def movie_reservation(request):
#     # CGV 웹사이트에서 예매율 정보를 크롤링
#     url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         movies = soup.find_all('div', class_='sect-movie-chart')

#         movie_list = []
#         for movie in movies:
#             # 'strong' 태그가 없으면 'title'을 빈 문자열로 설정
#             title_tag = movie.find('strong')
#             title = title_tag.text if title_tag else '제목 없음'

#             # 예매율을 찾을 때 None인지 확인
#             reservation_rate_tag = movie.find('span', class_='txt-grade')
#             reservation_rate = reservation_rate_tag.text if reservation_rate_tag else '정보 없음'  # 예매율이 없으면 '정보 없음' 표시
            
#             movie_list.append({'title': title, 'reservation_rate': reservation_rate})

#         # 크롤링한 데이터 템플릿에 전달
#         return render(request, 'my_app/box_office.html', {'movie_list': movie_list})

#     return render(request, 'my_app/box_office.html', {'error': '데이터를 가져오는 데 실패했습니다.'})

def box_office(request):
    # KOFIC API로 일일 박스오피스 데이터 가져오기
    api_key = '04c52266e1fdcfe2b96d62445a151a99'
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')  # 어제 날짜로 설정

    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    params = {
        'key': api_key,
        'targetDt': yesterday,  # 날짜를 동적으로 변경
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # 박스오피스 데이터를 가져옵니다.
        box_office_data = response.json().get('boxOfficeResult', {}).get('dailyBoxOfficeList', [])
    else:
        box_office_data = []
    
    # 데이터베이스에서 영화 정보를 가져옵니다.
    movies = Movie.objects.all().order_by('rank')
    
    reservation_url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
    reservation_response = requests.get(reservation_url)

    if reservation_response.status_code == 200:
        soup = BeautifulSoup(reservation_response.text, 'html.parser')

        # 영화 제목과 예매율 정보를 제대로 찾기 위한 수정
        movies = soup.find_all('div', class_='box-contents')  # 해당하는 div로 수정
        
        movie_list = []
        for movie in movies:
            # 영화 제목을 찾음
            title_tag = movie.find('strong')  # 영화 제목을 포함한 태그를 찾음
            title = title_tag.text.strip() if title_tag else '정보 없음'
            
            # 예매율을 찾음
            reservation_rate_tag = movie.find('strong', class_='percent')
            if reservation_rate_tag:
                reservation_rate = reservation_rate_tag.find('span').text.strip()
            else:
                reservation_rate = '정보 없음'

            movie_list.append({'title': title, 'reservation_rate': reservation_rate})
    else:
        movie_list = []


    return render(request, 'my_app/box_office.html', {
        'box_office_data': box_office_data,
        'movies': movies,
        'movie_list': movie_list
    })

