from django.shortcuts import render

# Create your views here.

from scanner.forms import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.template import RequestContext

from scanner.models import *

from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule
from scanner.globals import MYUCLA_USER, MYUCLA_PASS, BRUINSCAN_PASS, frequency

import itertools
import json
from django.utils import timezone
import time

from mysite.celery import app, text, email_from

User = get_user_model()

# worker: celery -A mysite worker -l info --without-gossip --without-mingle --without-heartbeat
# worker: celery -A mysite worker -P eventlet --without-gossip --without-mingle --without-heartbeat -c 100




def scanner1(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')


	subjects = Class_Data.objects.values_list('subject').distinct().order_by('subject')
	subjects = [x[0] for x in subjects]

	context = {
		'subjects': subjects,
	}

	return render(request, "scanner1.html", context)

def scanner2(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')


	subjects = Class_Data.objects.values_list('subject').distinct().order_by('subject')
	subjects = [x[0] for x in subjects]

	context = {
		'subjects': subjects,
	}

	return render(request, "scanner2.html", context)


def get_classes(request, term, subject):
	if request.is_ajax():

		term = "".join(term.split(" "))

		courses = Class_Data.objects.values_list('course').filter(course__icontains=term).filter(subject=subject)
		courses = [" ".join(x[0].split(" ")[1:]) for x in courses ]
		# courses_to_display = [ x.split(" ")[0].replace("&"," ") + " " + " ".join(x.split(" ")[1:]) for x in courses]
		
		html = ""
		for course in courses:
			html+="<option>" + str(course) + "</option>"
		if not html:
			html = "<option>No Classes Found</option>"
		return HttpResponse(html)

	else:
		raise Http404



def get_overview(request, term, course):
	if request.is_ajax():

		#course argument does NOT contain term


		term = "".join(term.split(" "))


		url, sections, statuses, day_times, locations, instructors, grades = zip(
			*Class_Data.objects.values_list\
			('url', 'sections', 'statuses', 'day_times', 'locations', 'instructors', 'grades')\
			.filter(course=term + " " + course)
		)

		url = url[0]
		section_list = sections[0].split("|*|")
		status_list = statuses[0].split("|*|")
		day_times_list = day_times[0].split("|*|")
		locations_list = locations[0].split("|*|")
		instructors_list = instructors[0].split("|*|")
		grades = [[float(x) for x in eval(y)] for y in grades[0].split("|*|")]
		max_percentages = [x[0] if x else None for x in grades]
		grades = [x[1:] if x else [] for x in grades]

		lectures = []
		discussions = []
		i = 0
		if any(x in section_list[0] for x in ["Dis"]):
			while i < len(section_list):
				lectures.append(section_list[i])
				discussions.append([])
				i+=1
		else:
			while i < len(section_list):
				lectures.append(section_list[i])
				cur = i
				i+=1
				possible = ["Lec", "Lab", "Sem", "Tut", "Rgp", "Stu"]
				if "Lec" in section_list[cur]:
					possible.remove("Lab")
				current = []
				while i < len(section_list) and not any(x in section_list[i] for x in possible):
					current.append(section_list[i])
					i+=1
				discussions.append(current)

		html = ""
		for lecture, discussion in zip(lectures, discussions):
			html += lecture + "<br>"
			# DISCUSSIONS ARE A LIST
			# html += discussion + "<br>"

		return HttpResponse(html)
	else:
		raise Http404




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
			login(request, user)
			return HttpResponseRedirect('/')
			# return HttpResponseRedirect('/register/success/')
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

def edit(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	message = ""
	
	if request.method == 'POST':
		form = UpdateForm(request.POST)
		if form.is_valid():

			good = True
			try:
				user = User.objects.get(username__iexact=form.cleaned_data['username'])
				if user.username != request.user.username:
					message += "Username Taken. "
					good = False
			except User.DoesNotExist:
				pass

			try:
				user = User.objects.get(email__iexact=form.cleaned_data['email'])
				if user.email != request.user.email:
					message += "Email Taken. "
					good = False
			except User.DoesNotExist:
				pass

			if not good:
				form = UpdateForm(
				initial={
					'username':request.user, 
					'email':request.user.email,
					'phone_number':request.user.phone_number,
					'carrier':request.user.carrier_address,
					})

			else:

				tasks = PeriodicTask.objects.all()
				for task in tasks:
					if task.name.split(" ")[0]==request.user.username:
						task.name = form.cleaned_data['username'] + " " + " ".join(task.name.split(" ")[1:])
						args = eval(task.args)
						args[0] = form.cleaned_data['username']
						args[1] = str(form.cleaned_data['phone_number'])
						args[2] = form.cleaned_data['carrier']
						task.args=json.dumps(args)
						task.save()

				tasks = Task_Data.objects.all()
				for task in tasks:
					if task.task_name.split(" ")[0]==request.user.username:
						task.task_name = form.cleaned_data['username'] + " " + " ".join(task.task_name.split(" ")[1:])
						task.save()

				user = User.objects.get(username=request.user.username)
				user.username = form.cleaned_data['username']
				user.email = form.cleaned_data['email']
				user.phone_number = form.cleaned_data['phone_number']
				user.carrier_address = form.cleaned_data['carrier']
				user.save()

				return HttpResponseRedirect('/account')

	else:
		form = UpdateForm(
			initial={
				'username':request.user, 
				'email':request.user.email,
				'phone_number':request.user.phone_number,
				'carrier':request.user.carrier_address,
				})

	context = {
		'form': form,
		'message': message
	}

	return render(request, "edit.html", context)

def account(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	return render(request, "account.html", {})


def contact(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			context = {
				'message': "Please sign in or create an account.",
			}
			return render(request, "contact.html", context)
		else:
			message = request.POST.get('message')
			message += "\n" + str(request.user.email)
			email_from.delay(message, str(request.user))
			context = {
				'message': "Message sent. We will reply to the email associated with your account.",
			}
	else:
		context = {}
	return render(request, "contact.html", context)


def manage(request):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	username = str(request.user)

	names, args = zip(*PeriodicTask.objects.values_list('name', 'args'))

	courses = []
	sections = []
	terms = []
	for i in range(0,len(names)):
		if username=="rishub" and len(eval(args[i]))>7:
			courses.append(str(" ".join(str(names[i]).split(" ")[1:])).strip())
			sections.append(str(eval(args[i])[3]))
			terms.append(str(eval(args[i])[5]))
		elif username==names[i].split(" ")[0]:
			courses.append(str(str(names[i]).split(username)[1]).strip())
			sections.append(str(eval(args[i])[3]))
			terms.append(str(eval(args[i])[5]))
		

	sections_to_check = [",".join(x.split("\n")) for x in sections]

	# ["rishub", "4086217236", "txt.att.net", "Dis 1\nDis 2\nDis 3\n", 
	# "4DW - Literature and Writing: Great Books from World at Large", "Comparative Literature", "COM LIT", 
	# "https://sa.ucla.edu/ro/ClassSearch/Results?t=17S&sBy=subject&sName=Comparative+Literature+%28COM+LIT%29&subj=COM+LIT&crsCatlg=4DW+-+Literature+and+Writing%3A+Great+Books+from+World+at+Large&catlg=0004DW&cls_no=%25&btnIsInIndex=btn_inIndex&btnIsExchange=False", {}]

	context = {
		'data': zip(courses, terms, sections, sections_to_check),
	}

	return render(request, "manage.html", context)


def remove(request, course):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	name = str(request.user) + " " + course

	PeriodicTask.objects.get(name=name).delete()

	# Task_Data(task_name=name, status_dict='{}').save()
	Task_Data.objects.get(task_name=name).delete()

	return HttpResponseRedirect('/manage')


def home(request, term):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	subjects = Class_Data.objects.values_list('subject').distinct().order_by('subject')
	subjects = [x[0] for x in subjects]

	if term == "SummerSessionA":
		head = "Summer Session A 2017"
	elif term == "SummerSessionC":
		head = "Summer Session C 2017"
	elif term=="Spring":
		head = "Spring 2017"

	context = {
		'subjects': subjects,
		'head': head,
		'term': term
	}

	return render(request, "home.html", context)


def courses(request, term, subject):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	courses = Class_Data.objects.values_list('course').filter(course__icontains=term).filter(subject=subject)
	courses = [" ".join(x[0].split(" ")[1:]) for x in courses ]
	courses_to_display = [ x.split(" ")[0].replace("&"," ") + " " + " ".join(x.split(" ")[1:]) for x in courses]
	
	context = {
		'courses': zip(courses, courses_to_display),
		'subject': subject,
		'term': term
	}

	return render(request, "courses.html", context)


def sections(request, term, course, check):

	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')


	# course argument does NOT contain the term


	url, sections, statuses, day_times, locations, instructors, grades = zip(
		*Class_Data.objects.values_list\
		('url', 'sections', 'statuses', 'day_times', 'locations', 'instructors', 'grades')\
		.filter(course=term + " " + course)
	)

	url = url[0]
	section_list = sections[0].split("|*|")
	status_list = statuses[0].split("|*|")
	day_times_list = day_times[0].split("|*|")
	locations_list = locations[0].split("|*|")
	instructors_list = instructors[0].split("|*|")
	grades = [[float(x) for x in eval(y)] for y in grades[0].split("|*|")]
	max_percentages = [x[0] if x else None for x in grades]
	grades = [x[1:] if x else [] for x in grades]

	lectures = []
	discussions = []
	i = 0
	if any(x in section_list[0] for x in ["Dis"]):
		while i < len(section_list):
			lectures.append(section_list[i])
			discussions.append([])
			i+=1
	else:
		while i < len(section_list):
			lectures.append(section_list[i])
			cur = i
			i+=1
			possible = ["Lec", "Lab", "Sem", "Tut", "Rgp", "Stu"]
			if "Lec" in section_list[cur]:
				possible.remove("Lab")
			current = []
			while i < len(section_list) and not any(x in section_list[i] for x in possible):
				current.append(section_list[i])
				i+=1
			discussions.append(current)


	iterator1=itertools.count()
	iterator2=itertools.count()
	iterator3=itertools.count()
	iterator4=itertools.count()
	iterator5=itertools.count()

	context = {
		'course': course,
		'data': zip(lectures, discussions),
		'url': url,
		'statuses': status_list,
		'day_times': day_times_list,
		'locations': locations_list,
		'instructors': instructors_list,
		'grades': grades,
		'term': term,
		'check': check,
		'iterator1': iterator1,
		'iterator2': iterator2,
		'iterator3': iterator3,
		'iterator4': iterator4,
		'iterator5': iterator5,
	}

	return render(request, "sections.html", context)



def scan(request, term, course):

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
	name = str(request.user) + " " + course


	# REMOVE TASK IF EXISTS
	try:
		pt = PeriodicTask.objects.get(name=name)
		pt.delete()
		Task_Data(task_name=name, status_dict='{}').save()
		time.sleep(5)	#?
	except:
		pass


	try:
		url = str(Class_Data.objects.values_list('url').get(course=term + " " + course)[0])
	except:
		text("4086217236", "txt.att.net", term + " " + course + " URL NOT FOUND")
		return render(request, "scan.html", { 'error': "COURSE NOT FOUND. ALERTED ADMINISTRATOR" })


	# schedule, created = IntervalSchedule.objects.get_or_create(every=8640000,period=IntervalSchedule.SECONDS,)
	# tz = timezone.now() - timezone.timedelta(seconds=8639990)
	# result = PeriodicTask.objects.create(interval=schedule, enabled=True, last_run_at=tz, name=name,task='scanner.tasks.scanner', 
	# 	args=json.dumps([str(request.user), phone_number, carrier_address, sections, course, subject_name, abbrev, url, {}]),)


	schedule, created = IntervalSchedule.objects.get_or_create(every=frequency,period=IntervalSchedule.SECONDS,)
	tz = timezone.now() - timezone.timedelta(seconds=frequency-10)
	result = PeriodicTask.objects.create(interval=schedule, enabled=True, last_run_at=tz, name=name,task='scanner.tasks.scanner', 
		args=json.dumps([str(request.user), phone_number, carrier_address, sections, course, term, url, {}]),)
	Task_Data(task_name=name, status_dict='{}').save()

	msg = "Scanning started for " + str(course)
	msg = msg.replace(":", "")
	text(phone_number, carrier_address, msg)


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
		'course': course,
	}

	return render(request, "scan.html", context)




