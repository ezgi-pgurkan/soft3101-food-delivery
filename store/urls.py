from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    #Leave as empty string for base url

    path('', views.home, name="home"),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout/', views.signout, name="signout"),
    path('registration/', views.registration, name="registration"),
    path('application/', views.application, name="application"),
    path('admin-dashboard/', views.adminDashboard, name='adminpage'),
    path('create_restaurantuser/', views.createRestaurantUser, name='create_restaurantuser'),
    path('create_restaurant/', views.createRestaurant, name='create_restaurant'),
    path('delete_restaurant/<str:pk>', views.deleteRestaurant, name='delete_restaurant'),  
    path('store/<restname>/', views.store, name='store'),
    path('update_item/', views.updateItem, name="update_item"), 
    path('process_order/<restname>/', views.processOrder, name="process_order"),
    path('account/', views.accountSettings, name='account'),
    path('delete_profile/<str:pk>', views.deleteProfile, name='delete_profile'),
    path('restaurant-owner-dashboard/', views.restaurantOwnerDashboard, name="restOwner"),
    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<str:pk>', views.updateProduct, name='update_product'),
    path('delete/<str:pk>', views.deleteProduct, name='delete_product'),
    path('add_review/<restname>/', views.addReviewView, name="add_review"),
    path('not_authorized/', views.notAuthorized, name="not_authorized"),
    path('cannotorder/', views.cannotOrder, name="cannotorder"),
    path('restaurant_search/', views.searchRestaurant, name='restaurant_search'),
    path('pizza/', views.pizza, name="pizza"),
    path('fastfood/', views.fastfood, name="fastfood"),
    path('asian/', views.asian, name="asian"),
    path('mypage/', views.myPage, name="mypage"),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

