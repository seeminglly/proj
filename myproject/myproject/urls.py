# """
# URL configuration for myproject project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from my_app import views  # my_app으로 수정


# urlpatterns = [
#     path('', views.box_office, name='box_office'),  # 빈 경로에 대해 box_office 뷰를 호출
#     path('box_office/', views.box_office, name='box_office'),
# ]

from django.contrib import admin
from django.urls import path
from my_app import views  # my_app으로 수정

urlpatterns = [
    path('', views.box_office, name='box_office'),  # 루트 경로에 대해서 box_office 뷰를 호출
    # path('box_office/', views.box_office, name='box_office'),  # 중복된 경로 제거
]
