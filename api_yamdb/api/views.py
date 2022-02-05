from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from api.permissions import AdminOrReadOnly, AdminOnly, AuthorOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

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
    GenreSerializer,
    UserSignupSerializer
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


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    serializer = UserSignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        # форматирование письма
        send_mail(
            "Your confirmation-code",
            token,
            "server-django@example.com",
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
@permission_classes((AllowAny,))
def token(request):
    # получаю username и confirmation_code ищ сериалайзера
    # is_active = True ??
    # default_token_generator.check_token(user, token)
    # refresh = RefreshToken.for_user(user)
    # Ответ - JWT токен
    # print(refresh, "-----", refresh.access_token)
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})

    return Response({'message': 'Это был GET-запрос!'})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer
