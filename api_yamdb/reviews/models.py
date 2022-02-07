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

    class Meta:
        ordering = ('-date_joined',)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    description = models.TextField(blank=True,)
    genre = models.ManyToManyField(
        Genre,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )


# class GenreTitle(models.Model):
#     genre = models.ForeignKey(
#         Genre,
#         on_delete=models.SET_NULL,
#        # null=True,
#        blank=True
#    )
#    title = models.ForeignKey(
#        Title,
#        on_delete=models.CASCADE
#    )


class Review():
    pass


class Comment():
    pass
