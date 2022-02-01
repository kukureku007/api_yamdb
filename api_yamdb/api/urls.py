from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register(
    r'(?P<version>v1)/users',
    UserViewSet,
    basename='api-v1-user'
)

urlpatterns = [
    # path('auth/', include('djoser.urls')),  # создание нового пользователя
    # path('v1/', include('djoser.urls.jwt')),  # jwt token create
    path('', include(router_v1.urls)),
]