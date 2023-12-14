from django.contrib import admin
from .models import Organization, Restaurant, RestaurantOutlet

# Register your models here.
admin.site.register(Organization)
admin.site.register(Restaurant)
admin.site.register(RestaurantOutlet)