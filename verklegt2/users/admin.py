# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, BuyerProfile, SellerProfile

class BuyerProfileInline(admin.StackedInline):
    model = BuyerProfile
    can_delete = False

class SellerProfileInline(admin.StackedInline):
    model = SellerProfile
    can_delete = False

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [BuyerProfileInline, SellerProfileInline]
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter  = ('user_type',)
