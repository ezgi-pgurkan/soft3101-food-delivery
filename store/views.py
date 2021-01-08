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

# Create your views here.

def signout(request):
    logout(request)
    return redirect('login')

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
        cartItems = order['get_cart_items']#available for guest users???

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
        cartItems = order['get_cart_items']#available for guest users??? we'll set that to the guest in user 

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
        cartItems = order['get_cart_items']#available for guest users??? we'll set that to the guest in user 

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

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) ###BAKKKKKK!!!!

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
                    zipcode=data['shipping']['zipcode']

                    )
            

        else:
            print('User is not logged in..')    
        return JsonResponse('Payment complete!',  safe=False)

