from django.urls import path

from . import views

app_name = "restaurant"
urlpatterns = [
    path("", views.index, name="index"),
    path("orgs/", views.organizationsIndex, name="organizationsIndex"),
    path("orgs/<int:organization_id>", views.organizationDetails, name="organizationDetails"),
    path("orgs/<int:organization_id>/<int:restaurant_id>", views.restaurantsIndex, name="restaurantsIndex"),
    path("outlets/<str:outlet_name>", views.outletPage, name="outletPage"),
    path("outlets/<str:outlet_name>/add", views.addTeamMember, name="addTeamMember"),
]
