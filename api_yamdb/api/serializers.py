from rest_framework import serializers
from django.db.models import Avg
from reviews.models import User, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    titles = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name'
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'titles')


class GenreSerializer(serializers.ModelSerializer):
    titles = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name'
    )

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug', 'titles')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='name'
        )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    # rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
           # 'rating'
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        return Avg(obj.reviews.score)
