from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "restaurant"
urlpatterns = [
    path("", views.index, name="index"),
    path("orgs/", views.organizationsIndex, name="organizationsIndex"),
    path("orgs/<int:organization_id>", views.organizationDetails, name="organizationDetails"),
    path("orgs/<int:organization_id>/<int:restaurant_id>", views.restaurantsIndex, name="restaurantsIndex"),
    path("outlets/<str:outlet_name>", views.outletPage, name="outletPage"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
