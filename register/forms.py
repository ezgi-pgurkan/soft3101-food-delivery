from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CITIES=[
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
    ('Antalya', 'Antalya'),
]

class RegisterForm(UserCreationForm):
    email  = forms.EmailField()
    name = forms.CharField(max_length=200)
    surname = forms.CharField(max_length=200)
    city=forms.CharField(widget=forms.Select(choices=CITIES))

    class Meta:
        model  = User
        fields = ('email', 'name', 'surname', 'password1', 'password2', 'city')
        field_order=('email', 'name', 'surname', 'password1', 'password2', 'city')
