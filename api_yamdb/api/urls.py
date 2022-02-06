from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    # UserMeViewSet,
    signup,
    token
)


app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register(
    # r'(?P<version>v1)/users',
    r'v1/users',
    UserViewSet,
    basename='api-v1-user'
)
# router_v1.register(
#     r'(?P<version>v1)/users/me',
#     UserMeViewSet,
#     basename='api-v1-me-user'
# )
router_v1.register(
    r'v1/categories',
    CategoryViewSet,
    basename='api-v1-category'
)
router_v1.register(
    r'v1/genres',
    GenreViewSet,
    basename='api-v1-genre'
)
router_v1.register(
    r'v1/titles',
    TitleViewSet,
    basename='api-v1-title'
)

urlpatterns = [
    path('v1/auth/signup/', signup, name='api-signup'),
    path('v1/auth/token/', token, name='api-token'),
    # path('v1/users/me/', UserMeViewSet.as_view({'get': 'retrieve'})),
    path('', include(router_v1.urls)),
]
