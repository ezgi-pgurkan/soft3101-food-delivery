from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField

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
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Phone')}), label=("Phone number"), required=True)

    class Meta:
        model  = RegisteredUser
        fields = ('email', 'username', 'password1', 'password2', 'name', 'surname', 'city', 'address', 'phone')
        field_order=('email', 'username', 'password1', 'password2', 'name', 'surname', 'city','address', 'phone')


class ProductForm(ModelForm):
    class Meta:
        model= Product
        fields = ('name', 'price', 'description', 'category', 'image')


class RestaurantForm1(UserCreationForm):
    is_restaurant=forms.BooleanField()
    class Meta:
        model  = RegisteredUser
        fields = ('email', 'username', 'password1', 'password2', 'is_restaurant')
        field_order=('email', 'username', 'password1', 'password2', 'is_restaurant')


class RestaurantForm2(ModelForm):
    class Meta:
        model= Restaurant
        fields = '__all__'


class CustomerForm(ModelForm):
    #city is not editable
    city = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Customer
        fields = ('name', 'surname', 'city', 'address', 'phone', 'profile_image')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'author')
        widgets = {
                    'body': forms.Textarea(attrs={'class': 'form-conrol'}),
                    'author': forms.TextInput(attrs={'class': 'form-conrol', 'value': '', 'id': 'elder', 'type': 'hidden'}),
                }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'author', 'review')
        widgets = {
                    'body': forms.Textarea(attrs={'class': 'form-conrol'}),
                    'author': forms.TextInput(attrs={'class': 'form-conrol', 'value': '', 'id': 'elder', 'type': 'hidden'}),
                }
