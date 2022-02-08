import datetime as dt
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Review, Title, User, Comment


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date', )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title_id, author=user).exists():
                raise serializers.ValidationError('Вы уже оставляли отзыв!')
        return data

    def validate_score(self, value):
        if value < 1 and value > 10:
            raise serializers.ValidationError(
                'Введите число от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
