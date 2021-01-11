from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RegisteredUser, Customer, Product, Restaurant
from django.forms import ModelForm

CITIES=[
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
    ('Antalya', 'Antalya'),
]

class CustomerCreationForm(UserCreationForm):
    email  = forms.EmailField()
    name = forms.CharField(max_length=200)
    surname = forms.CharField(max_length=200)
    city=forms.CharField(widget=forms.Select(choices=CITIES))
    address=forms.CharField(max_length=500)
    phone=forms.CharField(max_length=200)

    class Meta:
        model  = RegisteredUser
        fields = ('email', 'username', 'password1', 'password2', 'name', 'surname', 'city', 'address', 'phone')
        field_order=('email', 'username', 'password1', 'password2', 'name', 'surname', 'city','address', 'phone')


class ProductForm(ModelForm):
    class Meta:
        model= Product
        fields = ('name', 'price', 'description', 'category', 'image')

class RestaurantForm1(ModelForm):
    class Meta:
        model= RegisteredUser
        fields = '__all__'

class RestaurantForm2(ModelForm):
    class Meta:
        model= Restaurant
        fields = '__all__'