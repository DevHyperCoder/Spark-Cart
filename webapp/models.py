from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.timezone import now

# Extended User Model (UserProfile)
class UserProfile(AbstractUser):
    bio = models.CharField(max_length=1000)
    money = models.IntegerField(default=1000)

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    price = models.PositiveIntegerField()
    seller = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        default=1)
    rating = models.PositiveIntegerField(default=0)
    avg_rating = models.PositiveIntegerField(default=0)

# Ratings Model
class Ratings(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        default=1
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        default=1
    )
    text = models.CharField(max_length=200)
    created_date = models.DateField(default=now)
    rating_num = models.IntegerField(default=0)


