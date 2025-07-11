"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # 'include'를 임포트합니다.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')), # <--- 이 줄을 추가합니다.
                                     # 기본 경로('/')로 접속하면 'myapp' 앱의 urls.py를 참조합니다.
]
