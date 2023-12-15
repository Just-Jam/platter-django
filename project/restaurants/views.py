from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Organization, Restaurant, RestaurantOutlet, User
from .forms import CreateRestaurant, CreateUserForm, CreateRestaurantOutlet
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
        if form.is_valid():
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

    # Add outlets function
    # Handle form submission
    if request.method == 'POST':
        form = CreateRestaurantOutlet(request.POST)
        print(f'Form Data: {request.POST}')
        if form.is_valid():
            # Process the form data, save to the database, etc.
            # For example, form.save() if CreateRestaurant is a ModelForm
            # Redirect to avoid form resubmission on page refresh

            restaurant_outlet = form.save(commit=False)
            restaurant_outlet.restaurant = restaurant
            restaurant_outlet.save()
            return redirect('restaurant:restaurantsIndex', organization_id=organization_id, restaurant_id=restaurant_id)
        else:
            print('Form has errors')
            print(form.errors)
            print(form.non_field_errors())
    else:
        # Display a new form for GET requests
        form = CreateRestaurantOutlet()

    context = {
        'org': org,
        'restaurant': restaurant,
        'outlets': outlets,
        'form': form
    }

    return render(request, 'restaurants/restaurantsIndex.html', context)


def outletPage(request, outlet_name):
    outlet = get_object_or_404(RestaurantOutlet, name=outlet_name)
    team = User.objects.filter(groups__name=outlet_name)
    print(team)
    print(outlet.name)

    # Add user to team function
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(f'Form Data: {request.POST}')
        if form.is_valid():
            # Process the form data, save to the database, etc.
            # For example, form.save() if CreateRestaurant is a ModelForm
            # Redirect to avoid form resubmission on page refresh
            user_instance = form.save()
            print(user_instance)
            user_instance.groups.add(outlet)
            return redirect('restaurant:outletPage', outlet_name=outlet_name)
            # return redirect('restaurant:index')
        else:
            print('Form has errors')
            print(form.errors)
            print(form.non_field_errors())
    else:
        # Display a new form for GET requests
        form = CreateUserForm()

    context = {
        'outlet': outlet,
        'team': team,
        'user_in_team': False,
        'user_form': form
    }
    # check if user in group
    current_user = request.user
    if current_user.groups.filter(name=outlet_name).exists():
        context['user_in_team'] = True
    
    return render(request, 'restaurants/outletPage.html', context)
        