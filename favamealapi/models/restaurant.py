from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):

    name = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)
    favorite = models.ManyToManyField(User, through="FavoriteRestaurant")