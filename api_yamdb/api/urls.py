from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register(
    r'(?P<version>v1)/users',
    UserViewSet,
    basename='api-v1-user'
)
router_v1.register(
    r'(?P<version>v1)/categories',
    CategoryViewSet,
    basename='api-v1-category'
)
router_v1.register(
    r'(?P<version>v1)/genres',
    GenreViewSet,
    basename='api-v1-genre'
)
router_v1.register(
    r'(?P<version>v1)/titles',
    TitleViewSet,
    basename='api-v1-title'
)

urlpatterns = [
    # path('auth/', include('djoser.urls')),  # создание нового пользователя
    # path('v1/', include('djoser.urls.jwt')),  # jwt token create
    path('', include(router_v1.urls)),
]