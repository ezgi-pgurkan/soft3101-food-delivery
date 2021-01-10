from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.http import JsonResponse #yeni eklenen 
import json #yeni eklenen 
import datetime #yeni eklenen
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import *

# Create your views here.

def signout(request):
    logout(request)
    return redirect('signin')

def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'store/home.html', {'restaurants': restaurants})


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items 
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        
    products = Product.objects.all()
    starters=Product.objects.filter(category='Starter')
    salads=Product.objects.filter(category='Salad')
    specialties=Product.objects.filter(category='Specialty')
    desserts=Product.objects.filter(category='Dessert')
    drinks=Product.objects.filter(category='Drink')

    context={'products': products, 'cartItems': cartItems, 'starters': starters, 'salads': salads, 'specialties': specialties, 'desserts': desserts, 'drinks': drinks}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items # we'll set that to the logged in user 
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}

    context = {'items':items, 'order':order, 'cartItems': cartItems} #and we need to pass that in
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items # we'll set that to the logged in user 
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}

    context = {'items':items, 'order':order, 'cartItems': cartItems}
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

        message = 'Restaurant Name: ' + str(restaurantName) + '\nRestaurant City: ' + str(restaurantCity) + '\nRestaurant Phone: ' + str(restaurantPhone) + '\nRestaurant Owner Name: ' + str(restaurantOwnerName) + '\nRestaurant Owner Surname: ' + str(restaurantOwnerSurname) + '\nRestaurant Owner Email: ' + str(restaurantOwnerEmail) + '\nRestaurant Owners Phone: ' + str(restaurantOwnerPhone) + '\nWorking Days: ' + '\nFrom: ' + str(workingDaysFrom) + ' To: ' + str(workingDaysTo) + '\nWorking Hours:' + '\nFrom: ' + str(workingHoursFrom) + ' To: ' + str(workingHoursTo)

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


def updateItem(request): #yeni eklenen
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',  safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)

def restaurantOwnerDashboard(request):
    restaurant = request.user.restaurant

    #to display restaurant's products
    products=restaurant.products.all()

    #to display restaurant's orders
    orders=Order.objects.filter(restaurant=restaurant)

    context={'restaurant': restaurant,  'products': products, 'orders': orders}
    return render(request, 'store/restaurant-owner-dashboard.html', context)

def adminDashboard(request):

    restaurants=Restaurant.objects.all()
    context={'restaurants': restaurants}
    return render(request, 'store/admin-dashboard.html', context)


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            registeredUser = RegisteredUser.objects.filter(email=form.data['username']).first()

            if registeredUser is not None and not registeredUser.is_active:
                registeredUser.is_active = True
                registeredUser.save()
                if authenticate(request, email=form.data['username'], password=form.data['password']):
                    print("valid")
                    login(request, registeredUser, backend='django.contrib.auth.backends.ModelBackend')
                    base_url = reverse('home')
                    query_string = urlencode({'control': 'True'})
                    url = '{}?{}'.format(base_url, query_string)
                    return redirect(url)
                else:
                    error_message = "* Wrong Email or Password."
                    registeredUser.is_active = False
                    registeredUser.save()
            else:
                error_message = "* Wrong Email or Password."
    else:
        error_message = ""
        form = AuthenticationForm()
    return render(request, 'store/signin.html', {'form': form, 'error_message': error_message, })


def signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = RegisteredUser.objects.filter(email=form.cleaned_data['email']).first()
            user.is_customer = True
            user.save()
            customer = Customer(userEmail=user)
            customer.name=form.cleaned_data.get('name')
            customer.surname=form.cleaned_data.get('surname')
            customer.city=form.cleaned_data.get('city')
            customer.address=form.cleaned_data.get('address')
            customer.phone=form.cleaned_data.get('phone')
            customer.save()
            return redirect('/')
    else:
        form = CustomerCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def createProduct(request):
    restaurant_instance = request.user.restaurant
    form=ProductForm()
    if request.method=='POST':
        form=ProductForm(request.POST, request.FILES)
        if form.is_valid():     
            p = form.save()
            p.restaurant = restaurant_instance
            p.save()
            return redirect('restOwner')

    context={ 'restaurant_instance': restaurant_instance, 'form': form}
    return render(request, 'store/productform.html', context)

def updateProduct(request, pk):
    product=Product.objects.get(id=pk)
    form=ProductForm(instance=product)

    if request.method=='POST':
        form=ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():     
            form.save()
            return redirect('restOwner')

    context={'form': form}
    return render(request, 'store/productform.html', context)


def deleteProduct(request, pk):
    product=Product.objects.get(id=pk)
    if request.method=='POST':
        product.delete()
        return redirect('restOwner')

    context={'item': product}
    return render(request, 'store/delete.html', context)


def createRestaurantUser(request):
    form1=RestaurantForm1()
    if request.method=='POST':
        form1=RestaurantForm1(request.POST, request.FILES)
        if form1.is_valid():    
           form1.save()
           return redirect('create_restaurant')
       
    context={'form1': form1}
    return render(request, 'store/restaurantformfirst.html', context)

def createRestaurant(request):
    form2=RestaurantForm2()
    if request.method=='POST':
        form2=RestaurantForm2(request.POST, request.FILES)

        if form2.is_valid():    
           form2.save()
           return redirect('adminpage')

    context={'form2': form2}
    return render(request, 'store/restaurantformsecond.html', context)

def deleteRestaurant(request, pk):
    restaurant=Restaurant.objects.get(userEmail_id=pk)
    if request.method=='POST':
        restaurant.delete()
        return redirect('adminpage')

    context={'item': restaurant, 'restaurant': restaurant}
    return render(request, 'store/delete-restaurant.html', context)

