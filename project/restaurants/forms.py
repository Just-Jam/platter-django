from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Restaurant

class CreateUserForm(UserCreationForm):
    group = forms.CharField(max_length=50, required=True)
    class Meta:
        model = User
        fields = ['username', 'email']

class CreateRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'parent_organization']