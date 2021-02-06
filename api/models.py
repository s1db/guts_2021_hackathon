from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField("Name of user", blank=True, max_length=255)

class Address(models.Model):
    # address for each charity as a model 
    address_line_1 = models.CharField(max_length=256, blank=True)
    address_line_2 = models.CharField(blank=True, max_length=256)
    city = models.CharField(blank=True, max_length=56)
    postcode = models.CharField(max_length=25)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, default=0.0)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, default=0.0)

class CharityAccount(models.Model):

    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    charityname = models.CharField(max_length=56)
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=16,blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class DiertaryRequirements(models.Model):

    has_halal = models.BooleanField(default=False)
    has_sanitary_products = models.BooleanField(default=False)
    has_vegetarian = models.BooleanField(default=False)
    has_vegan = models.BooleanField(default=False)
    has_kosher = models.BooleanField(default=False)
    has_gluten_free = models.BooleanField(default=False)
    has_lactose_free = models.BooleanField(default=False)

class CharityDietaryOptions(models.Model):
    charity = models.ForeignKey(CharityAccount, on_delete=models.CASCADE)
    dietary_options = models.ForeignKey(DiertaryRequirements, on_delete=models.CASCADE)

class UserDietaryPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dietary_preferences = models.ForeignKey(DiertaryRequirements, on_delete=models.CASCADE)