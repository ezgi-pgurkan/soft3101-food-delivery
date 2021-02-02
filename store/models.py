from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_customer=False
        user.is_restaurant=False
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class RegisteredUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False) #!
    is_restaurant=models.BooleanField(default=False) #!
    hide_email=models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['username']

    def __str__(self):
        return self.email

    def get_profile_image_filepath(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Customer(models.Model):
    userEmail=models.OneToOneField(RegisteredUser, on_delete=models.CASCADE, primary_key=True)  
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
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    profile_image = models.ImageField(default='profilepic.png')

    def __str__(self):
        return self.userEmail.email


class Restaurant(models.Model):
    userEmail=models.OneToOneField(RegisteredUser, on_delete=models.CASCADE, primary_key=True)  
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
    city=models.CharField(max_length=200, null=True, choices=CITIES)
    restname = models.CharField(max_length=200, null=True)
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=300, null=True, blank=True) 
    image1 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image2 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image3 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image4 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image5 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image6 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image7 = models.ImageField(default='restaurant_defaultphoto.jpg')
    image8 = models.ImageField(default='restaurant_defaultphoto.jpg')
    logo = models.ImageField(default='logo.png')
    workingHoursFrom = models.CharField(max_length=200, null=True, blank=True)
    workingHoursTo = models.CharField(max_length=200, null=True, blank=True)
    workingDaysFrom = models.CharField(max_length=200, null=True, blank=True)
    workingDaysTo = models.CharField(max_length=200, null=True, blank=True)
    favorite= models.ManyToManyField(Customer, related_name='favorite', blank=True)

    def __str__(self):
        return self.userEmail.email


class Admin(models.Model):
    userEmail = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.userEmail.email


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
    restaurant = models.ForeignKey(Restaurant, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    isVisible=models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    restaurant = models.ForeignKey(Restaurant, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
        
    @property #loops through all the order items and
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
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

    @property
    def get_cart_item_names(self):
        orderitems = self.orderitem_set.all()
        total = str([str(item.product.name) + str(' x') + str (item.quantity) for item in orderitems])
        return total 


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
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


class Review(models.Model):
    body = models.TextField()
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return str(self.author.name) + ' | ' + str(self.body)

    def __str__(self):
        return self.body 


class Comment(models.Model):
    review=models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  '%s - %s' % (self.review.body, self.author.restname)






       