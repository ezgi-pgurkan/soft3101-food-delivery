from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail

# Create your views here.

def signout(request):
    logout(request)
    return redirect('login')

def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'store/home.html', {'restaurants': restaurants})


def store(request):
    products = Product.objects.all()
    starters=Product.objects.filter(category='Starter')
    salads=Product.objects.filter(category='Salad')
    specialties=Product.objects.filter(category='Specialty')
    desserts=Product.objects.filter(category='Dessert')
    drinks=Product.objects.filter(category='Drink')

    context={'products': products, 'starters': starters, 'salads': salads, 'specialties': specialties, 'desserts': desserts, 'drinks': drinks}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)

def profile(request):
    context = {}
    return render(request, 'store/profile.html')

def registration(request):
    context = {}
    return render(request, 'store/registration.html')

def application(request):
    if request.method == "POST":
        restaurantName = request.POST['restaurantName']
        restaurantCity = request.POST['restaurantCity']
        restaurantPhone = request.POST['restaurantPhone']
        restaurantOwnerName = request.POST['restaurantOwnerName']
        restaurantOwnerSurname = request.POST['restaurantOwnerSurname']
        restaurantOwnerEmail = request.POST['restaurantOwnerEmail']
        restaurantOwnerPhone = request.POST['restaurantOwnerPhone']
        workingDaysFrom = request.POST['workingDaysFrom']
        workingDaysTo = request.POST['workingDaysTo']
        workingHoursFrom = request.POST['workingHoursFrom']
        workingHoursTo = request.POST['workingHoursTo']

        message = 'Restaurant Name: ' + str(restaurantName) + ' Restaurant City: ' + str(restaurantCity) + ' Restaurant Phone: ' + str(restaurantPhone) + ' Restaurant Owner Name: ' + str(restaurantOwnerName) + ' Restaurant Owner Surname: ' + str(restaurantOwnerSurname) + ' Restaurant Owner Email: ' + str(restaurantOwnerEmail) + ' Restaurant Owners Phone: ' + str(restaurantOwnerPhone) + ' Working Days From: ' + str(workingDaysFrom) + ' To: ' + str(workingDaysTo) + ' Working Hours From: ' + str(workingHoursFrom) + ' To: ' + str(workingHoursTo)

        send_mail(
            'Restaurant Registration Request: ' + restaurantName, # subject
            message, # message
            restaurantOwnerEmail,  # from email
            ['ezgi.ggurkan@gmail.com'], # to email
            )


        context={'restaurantCity': restaurantCity, 'workingDaysFrom': workingDaysFrom, 
        'workingDaysTo': workingDaysTo, 'workingHoursFrom': workingHoursFrom,
        'workingHoursTo': workingHoursTo, 'restaurantOwnerName': restaurantOwnerName}



        return render(request, 'store/application.html', context)
    else:
        return render(request, 'store/registration.html', {})
