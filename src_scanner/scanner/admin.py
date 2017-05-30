from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from scanner.models import CustomUser
from django_celery_beat.models import PeriodicTask


class MyUserAdmin(UserAdmin):
	model = CustomUser
	list_per_page = 1000
	list_display = ('username', 'date_joined', 'email', 'phone_number', 'carrier_address', 'is_staff')


admin.site.register(CustomUser, MyUserAdmin)