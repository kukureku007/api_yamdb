from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User

from .filters import TitlesFilter
from .permissions import AdminOnly, AuthorOnly, ModeratorAdmin, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          UserSerializer, UserSerializerReadOnlyRole,
                          UserSignupSerializer, UserTokenSerializer)
from .viewsets import CreateListViewSet

EMAIL_SERVER = settings.DEFAULT_SERVER_EMAIL
EMAIL_THEME = 'Your confirmation-code'


def send_token_to_user(user_email, token):
    send_mail(
        EMAIL_THEME,
        token,
        EMAIL_SERVER,
        (user_email,),
        fail_silently=False,
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_permissions(self):
        if (
            self.action in ('retrieve', 'partial_update', 'destroy')
            and self.kwargs['username'] == 'me'
        ):
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_object(self):
        if self.kwargs['username'] == 'me':
            return get_object_or_404(User, username=self.request.user.username)
        return super().get_object()

    def get_serializer_class(self):
        if self.action == 'partial_update' and self.kwargs['username'] == 'me':
            return UserSerializerReadOnlyRole
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    serializer = UserSignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        send_token_to_user(user.email, token)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
@permission_classes((AllowAny,))
def token(request):
    serializer = UserTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.data['username'])
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)}
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (AdminOnly | ReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOnly | ReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Title, id=self.kwargs.get('title_id')
            )
        )

    def get_permissions(self):
        if self.request.method == "PATCH":
            return (AuthorOnly(),)

        if self.request.method == "DELETE":
            return (ModeratorAdmin(),)

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOnly | ReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews.all(),
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                title.reviews.all(),
                id=self.kwargs.get('review_id')
            )
        )

    def get_permissions(self):
        if self.request.method == "PATCH":
            return (AuthorOnly(),)

        if self.request.method == "DELETE":
            return (ModeratorAdmin(),)

        return super().get_permissions()
