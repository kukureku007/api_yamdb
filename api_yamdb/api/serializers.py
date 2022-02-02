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
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name')
    category = serializers.SlugRelatedField(
        read_only=True,
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
        read_only_fields = ('id', 'category')

    def get_rating(self, obj):
        return Avg(obj.reviews.score)
