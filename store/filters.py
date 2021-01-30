import django_filters
from django_filters import CharFilter #for searching restaurants by their names

from .models import *

TAGS=[
    ('Asian', 'Asian'),
    ('FastFood', 'FastFood'),
    ('Dessert', 'Dessert'),
    ('Bakery', 'Bakery'),
    ('Pizza', 'Pizza'),
]


class RestaurantFilter(django_filters.FilterSet):
    restname= CharFilter(field_name='restname', lookup_expr='icontains')
    #icontains for ignoring case sensitivity

    class Meta:
        model= Restaurant
        fields= ('tag', 'city', 'restname')

