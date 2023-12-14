from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Organization, Restaurant, RestaurantOutlet, User
from .forms import CreateRestaurant, CreateUserForm
# Create your views here.

def index(request):
    return render(request, "restaurants/index.html")

def organizationsIndex(request):
    org_list = Organization.objects.order_by('name')
    your_orgs = Organization.objects.filter(admin=request.user)
    context = {
        "org_list": org_list,
        "your_orgs": your_orgs,
    }
    return render(request, 'restaurants/orgList.html', context)

def organizationDetails(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)
    restaurants = Restaurant.objects.filter(parent_organization=org)
    
    # Handle form submission
    if request.method == 'POST':
        form = CreateRestaurant(request.POST)
        print(f'Form Data: {request.POST}')
        if form.is_valid():
            print('Form is valid')
            # Process the form data, save to the database, etc.
            # For example, form.save() if CreateRestaurant is a ModelForm
            # Redirect to avoid form resubmission on page refresh
            restaurant_instance = form.save()
            return redirect('restaurant:organizationDetails', organization_id=organization_id)
        else:
            print('Form has errors')
            print(form.errors)
            print(form.non_field_errors())
    else:
        # Display a new form for GET requests
        form = CreateRestaurant()

    context = {
        'org': org,
        'restaurants': restaurants,
        'form': form
    }

    return render(request, 'restaurants/orgDetails.html', context)

def restaurantsIndex(request, organization_id, restaurant_id):
    org = get_object_or_404(Organization, pk=organization_id)
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    outlets = RestaurantOutlet.objects.filter(restaurant=restaurant)
    context = {
        'org': org,
        'restaurant': restaurant,
        'outlets': outlets
    }
    return render(request, 'restaurants/restaurantsIndex.html', context)


def outletPage(request, outlet_name):
    outlet = get_object_or_404(RestaurantOutlet, name=outlet_name)
    team = User.objects.filter(groups__name=outlet_name)
    context = {
        'outlet': outlet,
        'team': team,
        'user_in_team': False
    }
    # check if user in group
    current_user = request.user
    if current_user.groups.filter(name=outlet_name).exists():
        context['user_in_team'] = True
    
    return render(request, 'restaurants/outletPage.html', context)

def addTeamMember(request, outlet_name):
    outlet = get_object_or_404(RestaurantOutlet, name=outlet_name)
    # check if user is manager
    if outlet.manager != request.user:
        return HttpResponse("Not manager, cannot add members")
    
    else:
        # Create new user
        input_username = ""
        input_email = ""
        input_password = ""
        new_user = User.objects.create_user(input_username, input_email, input_password)
        # add user to outlet group
        new_user.groups.add(outlet)
        return HttpResponseRedirect(reverse("restaurant:orgs"))
        