from django.shortcuts import render

# Create your views here.

from scanner.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from scanner.models import *

# from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

from scanner.tasks import texting
# from djcelery.models import PeriodicTask, IntervalSchedule
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule

import itertools
import json

from django.utils import timezone
import time

from mysite.celery import app




User = get_user_model()

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email'],
				phone_number=form.cleaned_data['phone_number'],
				carrier_address=form.cleaned_data['carrier'],
			)
			return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    context = {
    'form': form
    }
    return render(request, "registration/register.html", context)
 
def register_success(request):
	return render(request, "registration/success.html")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
def home(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	subjects, subject_names, abbrevs = zip(*Home_Data.objects.values_list('subject', 'subject_name', 'abbrev'))
	data = zip(subjects, subject_names, abbrevs)

	context = {
		'data': data,
	}

	return render(request, "home.html", context)

def account(request):

	# if not request.user.is_authenticated:
	# 	return HttpResponseRedirect('/')

	# if request.method == 'POST':
	# 	form = RegistrationForm(request.POST)
	# 	if form.is_valid():
	# 		#UPDATE FORM
	# 		return HttpResponseRedirect('/account')
	# else:
	# 	form = RegistrationForm(
	# 		initial={
	# 			'username':request.user, 
	# 			'email':request.user.email,
	# 			'phone_number':request.user.phone_number,
	# 			'carrier':request.user.carrier_address,
	# 			})

	# context = {
	# 	'form': form,
	# }
	context = {}

	return render(request, "account.html", context)


def contact(request):
	return render(request, "contact.html", {})

def manage(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	username = str(request.user)

	i = app.control.inspect()
	active_tasks = {}
	# while not active_tasks:
	active_tasks = i.active()

	courses = []

	# CHECK IF NO ACTIVE TAKS
	k, v = active_tasks.items()[0]
	print k, v
	if not v:
		context = {
		}
		return render(request, "manage.html", context)

	task_ids = []
	abbrevs=[]
	subject_names=[]
	for worker, tasks in active_tasks.iteritems():
		for task in tasks:
			args = task['args'][1:-1].split(", ")
			args = [arg[1:-1] for arg in args]
			if args[0]==str(request.user):	#first argument is username, need to get task name really 
				task_ids.append(task['id'])
				courses.append(args[4])
				subject_names.append(args[5])
				abbrevs.append(args[6])


	# 		0			1               2                       3		                   4                                       5                6
	# [u'rishub', u'4086217236', u'txt.att.net', u'Lec 1: Dis 1A|*|Dis 1B\n', u'31 - Introduction to Computer Science I', u'Computer Science', u'COM SCI']
	# args=json.dumps([str(request.user), phone_number, carrier_address, sections, course_name, subject_name, abbrev]),)


	# TODO: BE ABLE TO MODIFY DISCUSSION SECTIONS ON THIS PAGE

	context = {
		'data': zip(task_ids, courses, subject_names, abbrevs),
		# 'lectures': lectures,
		# 'discussions', discussions,
	}

	return render(request, "manage.html", context)



def remove(request, task_id, course_name):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	name = str(request.user)+" "+course_name

	pt = PeriodicTask.objects.get(name=name)
	pt.delete()
	app.control.revoke(task_id, terminate=True, signal="SIGKILL")

	# task = PeriodicTask.objects.get(name=name) # if we suppose names are unique
	# task.args=json.dumps(["test","test","test","test","test","test","test"])
	# task.save()

	return HttpResponseRedirect('/manage')


def courses(request, subject_name, abbrev):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	abbrevs, all_courses = zip(*Course_Data.objects.values_list('abbrev', 'courses'))

	data = []
	for abbreviation, courses in zip(abbrevs, all_courses):
		if abbreviation==abbrev:
			data = courses.split("|*|")
			break
	
	abbrev_fixed = abbrev.replace('+', ' ').replace('%26', '&')
	subject_name = subject_name.replace('+', ' ').replace('%26', '&')

	context = {
		'data': data,	#courses
		'abbrev': abbrev_fixed,
		'subject_name': subject_name,
	}

	return render(request, "courses.html", context)


def sections(request, course_name, abbrev, subject_name):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	courses, sections, statuses, waitlists = zip(*Section_Data.objects.values_list('course', 'sections', 'statuses', 'waitlists'))

	section_list = []
	status_list = []
	waitlist_list = []

	data = []
	i = 0
	for course in courses:
		if course==course_name:
			data.append("test")
			section_list = sections[i].split("|*|")
			status_list = statuses[i].split("|*|")
			waitlist_list = waitlists[i].split("|*|")
		i+=1

	lectures = []
	discussions = []
	i = 0
	while i < len(section_list):
		lectures.append(section_list[i])
		cur = i
		i+=1
		possible = ["Lec", "Lab", "Sem", "Tut"]
		if "Lec" in section_list[cur]:
			possible.remove("Lab")
		current = []
		while i < len(section_list) and not any(x in section_list[i] for x in possible):
			current.append(section_list[i])
			i+=1
		discussions.append(current)

	iterator1=itertools.count()
	iterator2=itertools.count()

	context = {
		'data': zip(lectures, discussions),
		'statuses': status_list,
		'waitlists': waitlist_list,
		'abbrev': abbrev,
		'course_name': course_name,
		'subject_name': subject_name,
		'iterator1': iterator1,
		'iterator2': iterator2,
	}

	return render(request, "sections.html", context)

def scan(request, abbrev, course_name, subject_name,):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	sections = ""
	if request.method == 'POST':
		sections = "\n".join(request.POST.get('sections').split("<br>")) #this value is separated by |*| to deal with commas
	else:
		context = {
			'sections': "Error: Please go back and add classes again",
		}
		return render(request, "scan.html", context)

	phone_number = str(request.user.phone_number)[2:]
	carrier_address = str(request.user.carrier_address)


	# START TASK
	name = str(request.user)+" "+course_name


	# REMOVE TASK IF EXISTS
	try:
		pt = PeriodicTask.objects.get(name=name)
		i = app.control.inspect()
		active_tasks = i.active()
		task_id = ""
		for worker, tasks in active_tasks.iteritems():
			for task in tasks:
				args = task['args'][1:-1].split(", ")
				args = [arg[1:-1] for arg in args]
				if args[0]==str(request.user) and args[4]==course_name:
					task_id = task['id']
					break
		app.control.revoke(task_id, terminate=True, signal="SIGKILL")
		pt.delete()
		time.sleep(5)
	except:
		pass

	schedule, _ = CrontabSchedule.objects.get_or_create(minute='*',hour='*',day_of_week='*',day_of_month='*',month_of_year='*',)
	schedule, created = IntervalSchedule.objects.get_or_create(every=8640000,period=IntervalSchedule.SECONDS,)
	tz = timezone.now() - timezone.timedelta(seconds=8639995)
	result = PeriodicTask.objects.create(interval=schedule, enabled=True, last_run_at=tz, name=name,task='scanner.tasks.texting', 
		args=json.dumps([str(request.user), phone_number, carrier_address, sections, course_name, subject_name, abbrev]),)


	# task = PeriodicTask.objects.get(name="task name") # if we suppose names are unique
	# task.args=json.dumps([id])
	# task.save()


	# change sections list to comma separated to make more readable for user
	new_sections = []
	for section in sections.split("\n"):
		new_sections.append(", ".join(section.split("|*|")))
	sections = "\n".join(new_sections)[:-1]

	context = {
		'sections': sections,
		'abbrev': abbrev,
		'subject_name': subject_name,
		'course_name': course_name
	}

	return render(request, "scan.html", context)




# teacher info
# bruinwalk graphs







