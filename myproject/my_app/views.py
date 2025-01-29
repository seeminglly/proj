# Create your views here.
from django.shortcuts import render
import requests

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
