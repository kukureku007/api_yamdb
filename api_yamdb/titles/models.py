from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # USER = 'user'
    # MODERATOR = 'moderator'
    # ADMIN = 'admin'
    # ROLE_CHOICES = (
    #     (USER, 'user'),
    #     (MODERATOR, 'moderator'),
    #     (ADMIN, 'admin'),
    # )
    pass


class Title():
    pass


class Category():
    pass


class Genre():
    pass


class Review():
    pass


class Comment():
    pass