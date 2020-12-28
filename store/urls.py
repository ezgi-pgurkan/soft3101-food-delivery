from django.conf.urls import url
from store import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	#path('update_item/', views.updateItem, name="update_item"),
	#path('process_order/', views.processOrder, name="process_order"),
	path('profile/', views.profile, name="profile"),
	

]

