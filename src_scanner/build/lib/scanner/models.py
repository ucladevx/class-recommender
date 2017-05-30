from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
	phone_number = PhoneNumberField()
	carrier_address = models.CharField(max_length=200)

class Home_Data(models.Model):
	subject = models.CharField(max_length=200)
	subject_name = models.CharField(max_length=200)
	abbrev = models.CharField(max_length=200)	

class Course_Data(models.Model):
	abbrev = models.CharField(max_length=200)
	courses = models.TextField(max_length=4000)

class Section_Data(models.Model):
	course = models.CharField(max_length=200)
	sections = models.TextField(max_length=4000)
	statuses = models.TextField(max_length=4000)
	waitlists = models.TextField(max_length=4000)


