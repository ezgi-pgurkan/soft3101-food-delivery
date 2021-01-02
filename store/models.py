from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

class City(models.Model):
    ISTANBUL='Istanbul'
    ANKARA='Ankara'
    IZMIR='Izmir'
    ANTALYA='Antalya'
    CITIES = [ 
        (ISTANBUL, 'Istanbul'),
        (ANKARA, 'Ankara'),
        (IZMIR, 'Izmir'),
        (ANTALYA, 'Antalya'),
    ]
    city=models.CharField(max_length=200, null=True, choices=CITIES) 

    def __str__(self):
        return self.city

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True) 
    username = models.CharField(max_length=200, unique=True, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True)
    password = models.CharField(max_length=200, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone= models.CharField(max_length=10, null=True)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email

class Tag(models.Model): 
    ASIAN ='Asian'
    FASTFOOD = 'FastFood'
    DESSERTS = 'Desserts'
    BAKERY = 'Bakery'
    PIZZA = 'Pizza'
    TAGS = [
        (ASIAN, 'Asian'),
        (FASTFOOD, 'FastFood'),
        (DESSERTS, 'Dessert'),
        (BAKERY, 'Bakery'),
        (PIZZA, 'Pizza'),
    ]
    tag = models.CharField(max_length=200, null=True, choices=TAGS) 

    def __str__(self):
        return self.tag

class Restaurant(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, null=True, blank=True)
    rate = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1, default=Decimal(0.0))
    rateCount = models.IntegerField(null=True, blank=True, default=0)
    image1 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image2 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image3 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image4 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    image5 = models.ImageField(default='defaultClient.jpg', upload_to='client_pics')
    logo = models.ImageField(default='static/assets/img/logo/default-logo.png', upload_to='static/assets/img/logo')
    workingHoursFrom = models.CharField(max_length=200, null=True, blank=True)
    workingHoursTo = models.CharField(max_length=200, null=True, blank=True)
    workingDaysFrom = models.CharField(max_length=200, null=True, blank=True)
    workingDaysTo = models.CharField(max_length=200, null=True, blank=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class RestaurantOwner(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    restaurant=models.OneToOneField(Restaurant, null=True, blank=True, on_delete=models.CASCADE)

class Product(models.Model):                              
    STARTER ='Starter'
    SALAD = 'Salad'
    SPECIALTY = 'Specialty'
    DESSERT = 'Dessert'
    DRINK = 'Drink'
    FOOD_CATEGORIES = [
        (STARTER, 'Starter'),
        (SALAD, 'Salad'),
        (SPECIALTY, 'Specialty'),
        (DESSERT, 'Dessert'),
        (DRINK, 'Drink'),
    ]
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    category=models.CharField(max_length=200, null=True, choices=FOOD_CATEGORIES)
    image = models.ImageField(default='static/assets/img/menu/default-product.jpg', upload_to='static/assets/img/menu')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
        
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
