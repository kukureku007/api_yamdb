from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        blank=True,
    )


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )


class Review():
    pass


class Comment():
    pass