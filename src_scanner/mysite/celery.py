from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from celery.task.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


from django.conf import settings
import django
django.setup()
# from scanner.tasks import *
from celery import shared_task
from celery.task import task
from celery.task.schedules import crontab
from celery.decorators import *

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from scanner.globals import MYUCLA_USER, MYUCLA_PASS, BRUINSCAN_PASS

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


app = Celery('mysite')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@task
def text(phone_number, carrier_address, msg):
	print msg
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("bruinscan@gmail.com", BRUINSCAN_PASS)
	server.sendmail("bruinscan@gmail.com", phone_number +"@"+ carrier_address, msg) 
	server.quit()

@task
def email_from(msg, username):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("bruinscan@gmail.com", BRUINSCAN_PASS)

	message = MIMEMultipart()
	message['From'] = "bruinscan"
	message['To'] = "bruinscan@gmail.com"
	message['Subject'] = username + " contact"
	body = msg
	message.attach(MIMEText(body, 'plain'))
	message = message.as_string()

	server.sendmail("bruinscan@gmail.com", "bruinscan@gmail.com", message) 
	server.quit()


# 12 hours: 43200.0
# 3 hours: 10800.0

app.conf.beat_schedule = {
	# 'populate': {
	#     'task': 'scanner.tasks.populate',	# does everything so every 12 hours
	#     'schedule': 10800.0,
	# },
	'ping': {
		'task': 'scanner.tasks.ping',
		'schedule': 1200.0,
	},
}













