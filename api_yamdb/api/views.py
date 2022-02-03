# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAdminUser
from api.permissions import AdminOrReadOnly, AdminOnly, AuthorOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import (
    User,
    Category,
    Genre,
    Title
)
from .serializers import (
    TitleSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination


# всё нерабочее! другие миксины/роутер или свой класс?
class UserMeViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AuthorOnly,)

    def get_queryset(self):
        return get_object_or_404(User, username=self.request.user.username)


# @api_view(('POST',))
# @permission_classes((AllowAny,))
# def signup(request):

#     if request.method == 'POST':
#         return Response({'message': 'Получены данные', 'data': request.data})

#     return Response({'message': 'Это был GET-запрос!'})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
   # permission_classes = (AdminOrReadOnly,)
   # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
   # permission_classes = (AdminOrReadOnly)
   #pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
   # pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre')
