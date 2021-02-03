from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from store import views
from .views import FavoriteView, PasswordsChangeView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.home, name="home"),
    path('signin', views.signin, name='signin'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"), name="reset_password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_complete.html"), name="password_reset_complete"),
    path('signup', views.signup, name='signup'),
    path('signout/', views.signout, name="signout"),
    path('registration/', views.registration, name="registration"),
    path('application/', views.application, name="application"),
    path('admin-dashboard/', views.adminDashboard, name='adminpage'),
    path('create_restaurantuser/', views.createRestaurantUser, name='create_restaurantuser'),
    path('create_restaurant/', views.createRestaurant, name='create_restaurant'),
    path('delete_restaurant/<str:pk>', views.deleteRestaurant, name='delete_restaurant'),  
    path('store/<restname>/', views.store, name='store'),
    path('cart/<restname>/', views.cart, name="cart"),
    path('checkout/<restname>/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"), 
    path('process_order/<restname>/', views.processOrder, name="process_order"),
    path('add_review/<restname>/', views.addReviewView, name="add_review"),
    path('restaurant_search/', views.searchRestaurant, name='restaurant_search'),
    path('pizza/', views.pizza, name="pizza"),
    path('fastfood/', views.fastfood, name="fastfood"),
    path('asian/', views.asian, name="asian"),   
    path('bakery/', views.bakery, name="bakery"),
    path('dessert/', views.dessert, name="dessert"),
    path('mypage/', views.myPage, name="mypage"),
    path('favorite/<restname>', FavoriteView, name='favorite'),
    path('account/', views.accountSettings, name='account'),
    path('delete_profile/<str:pk>', views.deleteProfile, name='delete_profile'),
    path('password/', PasswordsChangeView.as_view(template_name='store/changepassword.html'), name="changepassword"),
    path('password_success/', views.password_success, name="password_success"),
    path('restaurant-owner-dashboard/', views.restaurantOwnerDashboard, name="restOwner"),
    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<str:pk>', views.updateProduct, name='update_product'),
    path('delete_product/<str:pk>', views.deleteProduct, name='delete_product'),
    path('delete_review/<str:pk>', views.deleteReview, name='delete_review'),
    path('add_comment/<str:pk>', views.addCommentView, name="add_comment"),
    path('delete_comment/<str:pk>', views.deleteComment, name='delete_comment'),
    path('not_authorized/', views.notAuthorized, name="not_authorized"),
    path('cannotorder/', views.cannotOrder, name="cannotorder"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

