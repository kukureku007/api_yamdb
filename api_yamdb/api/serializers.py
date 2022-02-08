from rest_framework import serializers
from django.db.models import Avg
from reviews.models import User, Category, Genre, Title, Review
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
import datetime as dt


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(
            queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio',
        )


class UserSerializerReadOnlyRole(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserSignupSerializer(serializers.ModelSerializer):
    RESTRICTED_USERNAMES = (
        'me',
    )
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(
            queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value in self.RESTRICTED_USERNAMES:
            raise serializers.ValidationError(
                'This username is restricted. Try another one!'
            )
        return value


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError(
                'This confirmation_code is invalid'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                f'{value} год еще не наступил.'
            )
        return value

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))
        return rating.get("score__avg")


class TitlePostSerializer(TitleGetSerializer):

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    # rating = serializers.SerializerMethodField()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date',)

