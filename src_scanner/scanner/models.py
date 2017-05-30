from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
	phone_number = PhoneNumberField()
	carrier_address = models.CharField(max_length=500)

class Class_Data(models.Model):
	subject = models.CharField(max_length=250)
	course = models.CharField(max_length=250, primary_key=True)
	url = models.CharField(max_length=1000)
	sections = models.TextField(max_length=10000)
	statuses = models.TextField(max_length=10000)
	day_times = models.TextField(max_length=10000)
	locations = models.TextField(max_length=10000)
	instructors = models.TextField(max_length=10000)
	grades = models.TextField(max_length=10000, default="[]")

class Task_Data(models.Model):
	task_name = models.CharField(max_length=250, primary_key=True)
	status_dict = models.CharField(max_length=1000)