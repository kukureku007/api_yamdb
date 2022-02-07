from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from api.permissions import AdminOnly, ReadOnly, AuthorOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from api.filters import TitlesFilter
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Respo

from reviews.models import (
    User,
    Category,
    Genre,
    Title
)

from .serializers import (
    TitleGetSerializer,
    TitlePostSerializer,
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


class CreateListViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminOnly | ReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOnly | ReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    # queryset = Title.objects.all()
    permission_classes = (AdminOnly | ReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    #filterset_fields = ('year', 'name',)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        category_slug = self.request.query_params.get('category')
        genre_slug = self.request.query_params.get('genre')
        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
