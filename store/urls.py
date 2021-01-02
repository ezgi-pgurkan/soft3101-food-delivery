from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    #Leave as empty string for base url
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('signout/', views.signout, name="signout"),
    #path('update_item/', views.updateItem, name="update_item"),
    #path('process_order/', views.processOrder, name="process_order"),
    path('profile/', views.profile, name="profile"),
    path('registration/', views.registration, name="registration"),
    path('application/', views.application, name="application"),
]

