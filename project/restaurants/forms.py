from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Restaurant, RestaurantOutlet

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CreateRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'parent_organization']

class CreateRestaurantOutlet(forms.ModelForm):
    class Meta:
        model = RestaurantOutlet
        fields = ['name', 'location', 'manager']
