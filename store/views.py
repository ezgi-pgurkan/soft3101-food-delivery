from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
import json
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
from .forms import *
from .decorators import *
from django.contrib.auth.models import Group
from django.views.generic import ListView, CreateView
from .filters import RestaurantFilter
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'store/home.html', {'restaurants': restaurants})


#sign in for all users
@unauthenticated_user
def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.is_customer==True:
                return redirect('home')
            if request.user.is_admin==True:
                return redirect('adminpage')
            if request.user.is_restaurant==True:
                return redirect('restOwner')
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


#customer sign up
@unauthenticated_user
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
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return redirect('/')
    else:
        form = CustomerCreationForm()
    return render(request, 'store/signup.html', {'form': form})


#sign out for all users
def signout(request):
    logout(request)
    return redirect('signin')


#restaurant registration
@unauthenticated_user
def registration(request):
    context = {}
    return render(request, 'store/registration.html')


#restaurant registration - send form via email to register restaurant
@unauthenticated_user
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


#admin main page
@allowed_users(allowed_roles=['admin'])
def adminDashboard(request):
    restaurants=Restaurant.objects.all()
    context={'restaurants': restaurants}
    return render(request, 'store/admin-dashboard.html', context)


#admin creates restaurant owner's account
@allowed_users(allowed_roles=['admin'])
def createRestaurantUser(request):
    form1=RestaurantForm1()
    if request.method=='POST':
        form1=RestaurantForm1(request.POST, request.FILES)
        if form1.is_valid():    
            form1.save()
            user = RegisteredUser.objects.filter(email=form1.cleaned_data['email']).first()
            group = Group.objects.get(name='restaurant')
            user.groups.add(group)
            return redirect('create_restaurant')
       
    context={'form1': form1}
    return render(request, 'store/restaurantformfirst.html', context)


#admin creates and adds restaurant to the database
@allowed_users(allowed_roles=['admin'])
def createRestaurant(request):
    form2=RestaurantForm2()
    if request.method=='POST':
        form2=RestaurantForm2(request.POST, request.FILES)
        if form2.is_valid():    
            form2.save()
            restaurant = Restaurant(userEmail=form2.cleaned_data.get('userEmail'))
            restaurant.tag=form2.cleaned_data.get('tag')
            restaurant.city=form2.cleaned_data.get('city')
            restaurant.restname=form2.cleaned_data.get('restname')
            restaurant.phone=form2.cleaned_data.get('phone')
            restaurant.address=form2.cleaned_data.get('address')
            restaurant.rate=form2.cleaned_data.get('rate')
            restaurant.rateCount=form2.cleaned_data.get('rateCount')
            restaurant.image1=form2.cleaned_data.get('image1')
            restaurant.image2=form2.cleaned_data.get('image2')
            restaurant.image3=form2.cleaned_data.get('image3')
            restaurant.image4=form2.cleaned_data.get('image4')
            restaurant.image5=form2.cleaned_data.get('image5')
            restaurant.image6=form2.cleaned_data.get('image6')
            restaurant.image7=form2.cleaned_data.get('image7')
            restaurant.image8=form2.cleaned_data.get('image8')
            restaurant.logo=form2.cleaned_data.get('logo')
            restaurant.workingHoursFrom=form2.cleaned_data.get('workingHoursFrom')
            restaurant.workingHoursTo=form2.cleaned_data.get('workingHoursTo')
            restaurant.workingDaysFrom=form2.cleaned_data.get('workingDaysFrom')
            restaurant.workingDaysTo=form2.cleaned_data.get('workingDaysTo')
            restaurant.save()
            return redirect('adminpage')
    context={'form2': form2}
    return render(request, 'store/restaurantformsecond.html', context)


#admin deletes a restaurant
@allowed_users(allowed_roles=['admin'])
def deleteRestaurant(request, pk):
    restaurant=Restaurant.objects.get(userEmail_id=pk)
    emaill=restaurant.userEmail
    restUser=RegisteredUser.objects.get(email=emaill)
    if request.method=='POST':
        restaurant.delete()
        restUser.delete()
        return redirect('adminpage')

    context={'item': restaurant, 'restaurant': restaurant, 'restUser':restUser, 'emaill':emaill}
    return render(request, 'store/delete-restaurant.html', context)


#customer's view of a restaurant page
@canorder(allowed_roles=['customer'])
def store(request, restname):
    restaurant = get_object_or_404(Restaurant, restname=restname)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}    
    products=Product.objects.filter(restaurant=restaurant)
    starters=products.filter(category='Starter')
    salads=products.filter(category='Salad')
    specialties=products.filter(category='Specialty')
    desserts=products.filter(category='Dessert')
    drinks=products.filter(category='Drink')
    reviews =Review.objects.filter(restaurant=restaurant)
    favorited = False
    if restaurant.favorite.filter(userEmail_id=request.user.id).exists():
        favorited = True
    context={'restaurant': restaurant, 'order': order, 'products': products, 'items': items, 'cartItems': cartItems, 'starters': starters, 'salads': salads, 'specialties': specialties, 'desserts': desserts, 'drinks': drinks,'reviews':reviews, 'favorited':favorited}
    return render(request, 'store/store.html', context)


#customer's cart
@canorder(allowed_roles=['customer'])
def cart(request, restname):
    restaurant = get_object_or_404(Restaurant, restname=restname)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items # we'll set that to the logged in user 
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping': False}

    context = {'items':items, 'order':order, 'cartItems': cartItems, 'restaurant':restaurant} #and we need to pass that in
    return render(request, 'store/cart.html', context)


#customer checkout
@canorder(allowed_roles=['customer'])
def checkout(request, restname):
    restaurant = get_object_or_404(Restaurant, restname=restname)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items # we'll set that to the logged in user 
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}

    context = {'items':items, 'order':order, 'cartItems': cartItems, 'restaurant':restaurant}
    return render(request, 'store/checkout.html', context)


#update order items in cart
@canorder(allowed_roles=['customer'])
def updateItem(request):
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


#payment
@canorder(allowed_roles=['customer'])
def processOrder(request, restname):
    restaurant = get_object_or_404(Restaurant, restname=restname)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.restaurant=Restaurant.objects.get(restname=restname)
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


#review
@allowed_users(allowed_roles=['customer'])
def addReviewView(request, restname):
    rest = get_object_or_404(Restaurant, restname=restname)
    customer=request.user.customer
    
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review= Review.objects.create(author=customer, restaurant=rest)
            review.body=form.cleaned_data.get('body')
            review.save()  
            return redirect('store', restname) 

    context = {'form':form, 'rest':rest, 'customer':customer}
    return render(request, 'store/add_review.html', context)


#restaurant search & filter
def searchRestaurant(request):
    restaurants=Restaurant.objects.all()

    myFilter=RestaurantFilter(request.GET, queryset=restaurants)
    restaurants=myFilter.qs

    context={'restaurants':restaurants, 'myFilter':myFilter}

    return render(request, 'store/restaurant_search.html', context)

#restaurants filtered by Pizza
def pizza(request):
    restaurants=Restaurant.objects.filter(tag='Pizza')

    context={'restaurants':restaurants}

    return render(request, 'store/pizza.html', context)


#restaurants filtered by Fast Food
def fastfood(request):
    restaurants=Restaurant.objects.filter(tag='FastFood')

    context={'restaurants':restaurants}

    return render(request, 'store/fastfood.html', context)


#restaurants filtered by Asian
def asian(request):
    restaurants=Restaurant.objects.filter(tag='Asian')

    context={'restaurants':restaurants}

    return render(request, 'store/asian.html', context)


#restaurants filtered by Bakery
def bakery(request):
    restaurants=Restaurant.objects.filter(tag='Bakery')

    context={'restaurants':restaurants}

    return render(request, 'store/bakery.html', context)


#restaurants filtered by Desserts
def dessert(request):
    restaurants=Restaurant.objects.filter(tag='Desserts')

    context={'restaurants':restaurants}

    return render(request, 'store/dessert.html', context)

#customer's page
@allowed_users(allowed_roles=['customer'])
def myPage(request):
    customer = request.user.customer

    #customer's orders
    orders=Order.objects.filter(customer=customer, complete=True)

    #customer's reviews
    reviews=Review.objects.filter(author=customer)

    #customer's favorite restaurants
    favorite_restaurants=customer.favorite.all()

    context={'cucustomerst': customer, 'orders':orders, 'reviews':reviews, 'favorite_restaurants':favorite_restaurants}

    return render(request, 'store/mypage.html', context)


#customer's favorite restaurants
@allowed_users(allowed_roles=['customer'])
def FavoriteView(request, restname):
    restaurant = get_object_or_404(Restaurant, restname=restname)
    favorited=False
    if restaurant.favorite.filter(userEmail_id=request.user.id).exists():
        restaurant.favorite.remove(request.user.customer)
        favorited=False
    else:
        restaurant.favorite.add(request.user.customer)
        favorited=True
    return HttpResponseRedirect(reverse('store', args=[str(restname)]))


#customer account settings
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'store/account_settings.html', context)


#customer deletes their profile
@allowed_users(allowed_roles=['customer'])
def deleteProfile(request, pk):
    user = RegisteredUser.objects.get(id=pk)
    if request.method == "POST":
        user.delete()
        return redirect('/', id=pk)

    context = {'user': user}
    return render(request, 'store/delete_profile.html', context)


#change password
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


#password succeffully changed message
@allowed_users(allowed_roles=['admin', 'restaurant', 'customer'])
def password_success(request):
    return render(request, 'store/password_success.html', {})


#restaurant owner main page
@allowed_users(allowed_roles=['restaurant'])
def restaurantOwnerDashboard(request):
    restaurant = request.user.restaurant

    #to display restaurant's products
    products=restaurant.products.all()

    #to display restaurant's orders
    orders=Order.objects.filter(restaurant=restaurant)

    #to display restaurant's reviews
    reviews =Review.objects.filter(restaurant=restaurant)


    context={'restaurant': restaurant,  'products': products, 'orders': orders, 'reviews': reviews}
    return render(request, 'store/restaurant-owner-dashboard.html', context)


#restaurant owner adds a new product to their restaurant
@allowed_users(allowed_roles=['restaurant'])
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


#restaurant owner updates a product from their restaurant
@allowed_users(allowed_roles=['restaurant'])
def updateProduct(request, pk):
    restaurant_instance = request.user.restaurant
    product=Product.objects.get(id=pk)
    form=ProductForm(instance=product)
   

    if request.method=='POST':
        form=ProductForm(request.POST, request.FILES)
       
        if form.is_valid(): 
            product.isVisible=False
            product.save()
            p = form.save()
            p.restaurant = restaurant_instance
            p.save()
            return redirect('restOwner')

    context={'restaurant_instance': restaurant_instance, 'form': form}
    return render(request, 'store/productform.html', context)


#restaurant owner deletes a product from their restaurant
@allowed_users(allowed_roles=['restaurant'])
def deleteProduct(request, pk):
    product=Product.objects.get(id=pk)
    if request.method=='POST':
        product.isVisible=False
        product.save()
        return redirect('restOwner')

    return render(request, 'store/delete_product.html')


#restaurant owner deletes a review about their restaurant
@allowed_users(allowed_roles=['restaurant', 'customer'])
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == "POST":
        review.delete()
        if request.user.is_customer==True:
            return redirect('mypage')
           
        if request.user.is_restaurant==True:
            return redirect('restOwner')

    context = {'review': review}
    return render(request, 'store/delete_review.html', context)


#restaurant owner replies to a review about their restaurant
@allowed_users(allowed_roles=['restaurant'])
def addCommentView(request, pk):
    restaurant=request.user.restaurant
    review = Review.objects.get(id=pk)
    
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= Comment.objects.create(author=restaurant, review=review)
            comment.body=form.cleaned_data.get('body')
            comment.save()  
            return redirect('restOwner') 

    context = {'form':form, 'restaurant':restaurant, 'review':review}
    return render(request, 'store/add_comment.html', context)


#restaurant owner deletes their reply to a review about their restaurant
@allowed_users(allowed_roles=['restaurant'])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == "POST":
        comment.delete()
        return redirect('restOwner') 

    context = {'comment': comment}
    return render(request, 'store/delete_comment.html', context)


#role not authorized to view the page
def notAuthorized(request):
    context = {}
    return render(request, 'store/not_authorized.html')


#role is not a customer, so cannot order from a restaurant
def cannotOrder(request):
    context = {}
    return render(request, 'store/cannotorder.html')









