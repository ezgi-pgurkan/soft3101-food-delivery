from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    model = RegisteredUser
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_customer', 'is_restaurant')
    list_filter = ('email', 'is_staff', 'is_active',)
    readonly_fields=('id', 'date_joined', 'last_login')
    fieldsets = ()
   
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(RegisteredUser, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Admin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)
admin.site.register(Comment)

