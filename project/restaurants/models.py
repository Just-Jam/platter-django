from django.db import models
from django.contrib.auth.models import User, Group

from django.conf import settings

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=50)
    head_office = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    parent_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
    
class RestaurantOutlet(Group):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_DEFAULT, default=None)
    def __str__(self):
        return f"{self.restaurant} - {self.location}"

