from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from store import views
from .views import StoreView,CommentDetailView, AddPostView
from django.conf.urls.static import static#NEW
from django.conf import settings #new


urlpatterns = [
    #Leave as empty string for base url
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout/', views.signout, name="signout"),
    path('registration/', views.registration, name="registration"),
    path('application/', views.application, name="application"),
    path('update_item/', views.updateItem, name="update_item"), 
    path('process_order/', views.processOrder, name="process_order"),
    path('restaurant-owner-dashboard/', views.restaurantOwnerDashboard, name="restOwner"), #yeni eklenen
    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<str:pk>', views.updateProduct, name='update_product'),
    path('delete/<str:pk>', views.deleteProduct, name='delete_product'),
    path('admin-dashboard/', views.adminDashboard, name='adminpage'),
    path('create_restaurantuser/', views.createRestaurantUser, name='create_restaurantuser'),
    path('create_restaurant/', views.createRestaurant, name='create_restaurant'),
    path('delete_restaurant/<str:pk>', views.deleteRestaurant, name='delete_restaurant'),  
    path('account/', views.accountSettings, name='account'), #yeni eklenen
    path('delete_profile/<str:pk>', views.deleteProfile, name='delete_profile'),
    path('store/', StoreView.as_view(), name="store"),
    path('detail/<int:pk>', CommentDetailView.as_view(), name='d-detail'),
    path('add_post/', AddPostView.as_view(), name="add_post"),
  

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)