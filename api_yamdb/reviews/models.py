from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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

    class Meta:
        ordering = ('-date_joined',)


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Произведение')
    year = models.PositiveIntegerField(
            validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.now().year)],
            help_text="Используйте следующий формат: <YYYY>",
            verbose_name='Год.',
            db_index=True
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категории',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('year',)


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(verbose_name='Оценка')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'title', 'author'
                ),
                name='На произведение уже оставлен отзыв данным автором.'
            ),
        )
        ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
