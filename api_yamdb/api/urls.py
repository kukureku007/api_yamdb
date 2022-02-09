from django.urls import include, path

from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='api-v1-review'
)

router_v1.register(
    r'(?P<version>v1)/users',
    UserViewSet,
    basename='api-v1-user'
)
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
router_v1.register(
    (
        r'(?P<version>v1)/titles/'
        r'(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'
    ),
    CommentViewSet,
    basename='api-v1-titles'

)

urlpatterns = [
    path('v1/auth/signup/', signup, name='api-signup'),
    path('v1/auth/token/', token, name='api-token'),
    path('', include(router_v1.urls)),
]
