from django.urls import include, path
from rest_framework import routers

# from .views import TitleViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()

# Пример работы с роутером
# router_v1.register(
    # r'(?P<version>v1)/titles',
    # TitleViewSet,
    # basename='api-v1-title'
# )

urlpatterns = [
    # path('auth/', include('djoser.urls')),  # создание нового пользователя
    # path('v1/', include('djoser.urls.jwt')),  # jwt token create
    path('', include(router_v1.urls)),
]