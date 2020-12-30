from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *

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
