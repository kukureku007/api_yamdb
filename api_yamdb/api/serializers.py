from rest_framework import serializers
from django.db.models import Avg
from reviews.models import User, Review


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
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating'
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        return Avg(obj.reviews.score)
