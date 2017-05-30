from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from scanner.models import CustomUser


class MyUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('username', 'email', 'phone_number', 'carrier_address', 'is_staff')

admin.site.register(CustomUser, MyUserAdmin)