from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
#from .forms import RegisteredUserCreationForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    # add_form = RegisteredUserCreationForm
    model = RegisteredUser
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_customer', 'is_restaurant')
    list_filter = ('email', 'is_staff', 'is_active',)
    readonly_fields=('id', 'date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'is_customer', 'is_restaurant', 'is_admin')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'is_staff', 'is_active', 'is_customer', 'is_restaurant', 'is_admin')}
        ),
    )
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