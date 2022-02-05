from rest_framework import serializers
from django.db.models import Avg
from reviews.models import User, Category, Genre, Title
from rest_framework.validators import UniqueValidator


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

    # class Meta:
    #     model = User
    #     fields = (
    #         'username',
    #         'confirmation_code'
    #     )
    #     read_only_fields = ('username',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleGetSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    category = CategorySerializer()

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
        read_only_fields = ('id', )


class TitlePostSerializer(TitleGetSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    # rating = serializers.SerializerMethodField()
