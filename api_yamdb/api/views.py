from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from reviews.models import User, Category, Genre, Title
from .serializers import TitleSerializer, UserSerializer, CategorySerializer, GenreSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    
    return Response({'message': 'Это был GET-запрос!'}) 


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
