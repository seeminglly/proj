import requests
from django.core.management.base import BaseCommand
from my_app.models import TVShow

class Command(BaseCommand):
    help = "Fetch trending TV series data from TMDb and store it in the database"

    def handle(self, *args, **kwargs):
        api_key = 'bf5c5094ad11fd8f27152d30f1980757'
        url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}&language=ko-KR"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ API 요청 실패: {str(e)}"))
            return

        # TV 시리즈 정보 저장
        for show in data.get('results', []):
            title = show['name']
            overview = show.get('overview', '')
            release_date = show.get('first_air_date', None)
            poster_url = f"https://image.tmdb.org/t/p/w500{show['poster_path']}" if show.get('poster_path') else None
            vote_average = show.get('vote_average', 0)
            popularity = show.get('popularity', 0)

            # 데이터베이스에 저장 (중복 방지)
            tv_show, created = TVShow.objects.update_or_create(
                title=title,
                defaults={
                    'overview': overview,
                    'release_date': release_date,
                    'poster_url': poster_url,
                    'vote_average': vote_average,
                    'popularity': popularity
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ TV 시리즈 추가: {title}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"🔄 TV 시리즈 업데이트: {title}"))
