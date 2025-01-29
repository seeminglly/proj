# Create your views here.
from django.shortcuts import render
import requests
from django.http import JsonResponse

def box_office(request):
    api_key = '04c52266e1fdcfe2b96d62445a151a99'
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    params = {
        'key': api_key,
        'targetDt': '20241201',  # 날짜를 동적으로 변경할 수 있습니다.
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()['boxOfficeResult']['dailyBoxOfficeList']
    else:
        data = []

    return render(request, 'my_app/box_office.html', {'data': data})


def trending_tv_shows(request):
    api_key = 'bf5c5094ad11fd8f27152d30f1980757'
    if not api_key:
        return JsonResponse({'error': 'API 키가 설정되지 않았습니다.'}, status=500)

    # 파라미터 준비
    user_id = '21272571'  # 사용자 ID
    target_date = '20241201'  # 특정 날짜 설정
    url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}&language=ko-KR"
    
    response = requests.get(url)
    data = response.json()
        
    return render(request, 'my_app/trending_tv.html',{'tv_shows': data['results']})