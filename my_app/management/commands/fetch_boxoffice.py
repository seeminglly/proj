import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from my_app.models import Movie

class Command(BaseCommand):
    help = "Fetch daily box office data from KOFIC and store it in the database"

    def handle(self, *args, **kwargs):
        API_KEY = "04c52266e1fdcfe2b96d62445a151a99"
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

        url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={API_KEY}&targetDt={yesterday}"
        response = requests.get(url)
        data = response.json()

        if "boxOfficeResult" in data and "dailyBoxOfficeList" in data["boxOfficeResult"]:
            for movie_data in data["boxOfficeResult"]["dailyBoxOfficeList"]:
                movie_cd = movie_data["movieCd"]
                movie_nm = movie_data["movieNm"]
                rank = int(movie_data["rank"])
                audi_cnt = int(movie_data["audiCnt"])
                audi_acc = int(movie_data["audiAcc"])

                # 개봉일 데이터가 있는지 확인 후 저장
                open_dt = movie_data.get("openDt", None)
                if open_dt:
                    open_dt = datetime.strptime(open_dt, "%Y-%m-%d").date()

                # 영화 정보 저장 (중복 방지)
                movie, created = Movie.objects.update_or_create(
                    movie_cd=movie_cd,
                    defaults={
                        "movie_nm": movie_nm,
                        "rank": rank,
                        "audi_cnt": audi_cnt,
                        "audi_acc": audi_acc,
                        "open_dt": open_dt
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ 영화 추가: {movie_nm}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"🔄 영화 업데이트: {movie_nm}"))
        else:
            self.stdout.write(self.style.ERROR("❌ KOFIC API 데이터를 가져올 수 없습니다."))
