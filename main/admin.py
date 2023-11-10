# pylint: disable=W0401
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from main.models import User  
from .models import *
# Register your models here.

# admin.site.register(department)
class CustomUserAdmin(UserAdmin):
    search_fields = ('email', )
    ordering = ('-email', )
    list_filter = ('email', 'is_active', 'is_staff', )
    list_display = ('email', 'is_active', 'is_staff', )

    fieldsets = (
        ('Personal', {'fields': ('email', 'password', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email','password1', 'password2', 'is_active', 'is_staff', 'is_superuser', ),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register([
   
   
    SupplierType,
    Sale,
    BOM,
    AppFunctions,
    UserRole,
    Supplier,
    Purchase_Order,
    Item_group,
    Item_category,
    Item,
    Stock_Receipt,
    UOM,
    Company_details,
    Ingredient,
    Branch,
    StoreOwner,
    AppUser,
    Cashier,
    
])
