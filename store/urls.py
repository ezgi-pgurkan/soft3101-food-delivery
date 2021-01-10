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
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout/', views.signout, name="signout"),
    path('profile/', views.profile, name="profile"),
    path('registration/', views.registration, name="registration"),
    path('application/', views.application, name="application"),
    path('update_item/', views.updateItem, name="update_item"), 
    path('process_order/', views.processOrder, name="process_order"),
    path('restaurant-owner-dashboard/', views.restaurantOwnerDashboard, name="restOwner"), #yeni eklenen
    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<str:pk>', views.updateProduct, name='update_product'),
    path('delete/<str:pk>', views.deleteProduct, name='delete_product'),
    path('admin-dashboard/', views.adminDashboard, name="adminpage"),
    path('create_restaurantuser/', views.createRestaurantUser, name='create_restaurantuser'),
    path('create_restaurant/', views.createRestaurant, name='create_restaurant'),
    path('delete_restaurant/<str:pk>', views.deleteRestaurant, name='delete_restaurant'),

]