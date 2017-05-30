from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import task
from celery.task.schedules import crontab
from celery.decorators import *

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from scanner.globals import MYUCLA_USER, MYUCLA_PASS, BRUINSCAN_PASS, frequency

from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule
from celery.signals import celeryd_init, celeryd_after_setup, worker_ready
import json

from scanner.models import Task_Data, Class_Data
from scanner.classes import *
from datetime import datetime, timedelta
import traceback
import collections

from mysite.celery import app

from django.contrib.auth import get_user_model
User = get_user_model()

links = [
	"http://www.mercurynws.com/2017/04/07/saratoga-sees-quick-growth-of-neighborhood-watch-programs/ ",
	"http://www.mercurynews.com/2017/02/10/saratoga-city-creates-process-to-install-survillance-cameras-in-public-right-of-way/",
	"http://www.mercurynews.com/2017/03/10/saratoga-council-makes-public-safety-key-priority/",
	"http://www.mercurynews.com/2016/12/19/saratoga-keeping-your-holidays-safe/",
	"http://www.mercurynews.com/2016/07/06/is-saratoga-among-the-safest-cities-in-california-yes-but/",
	"http://www.mercurynews.com/2016/10/27/saratoga-more-than-30-neighborhood-watch-programs-certified-by-city-other-safety-measures-put-in-place/",
	"http://www.mercurynews.com/2015/09/23/saratogas-tech-day-is-a-special-event-for-youth-hosted-by-youth/",
	"http://www.pr.com/press-release/709123",
	"http://www.mercurynews.com/2015/08/26/saratoga-residents-can-you-hear-them-now-council-approves-cell-antennas/",
	"https://yubanet.com/california/treasurer-chiang-27-asian-american-office-holders-decry-president-trumps-muslim-ban/",
	"http://www.indiawest.com/entertainment/global/bollywood-superstar-shah-rukh-khan-to-host-indian-academy-awards/article_c43b1a60-eefe-11e6-8ca8-bf08a371da19.html",
	"http://www.mercurynews.com/2015/05/20/stride-for-susie-raises-lung-cancer-awareness/",
	"http://www.bizjournals.com/sanjose/news/2015/09/04/roku-saratogas-biggest-brand-heads-to-los-gatos-in.html",
	"http://www.indiawest.com/news/global_indian/indian-americans-in-california-elected-to-city-councils-boards/article_2bc52bde-7018-11e4-af47-b380b539d8d9.html",
	"http://news.e2.com.tw/gb/2017-3/9386119.htm",
	"http://www.indiawest.com/news/global_indian/ash-kalra-formally-launches-california-state-assembly-bid/article_34fdf57c-ae49-11e4-8e01-d32ea0387a5f.html",
	"http://www.indiapost.com/time-to-engage-politically-in-life-of-this-country-raja/",
	"https://www.theindianpanorama.news/indian-american-lawmakers-express-concern-regarding-hate-crimes-indian-americans-bay-area/#.WPVKn1Pyvwc",
	"http://www.mercurynews.com/2016/09/25/indian-americans-no-sure-bet-to-fall-in-line-for-khanna/",
	"http://www.mercurynews.com/2014/07/30/saratoga-five-candidates-in-the-running-for-council-but-theres-room-for-more/",
	"http://www.mercurynews.com/2016/08/03/whos-at-the-front-door-ring-has-the-answer/",
	"http://www.rishikumar.com/water.html",
	"www.rishikumar.com/uploads/3/3/0/6/3306532/cpuc_protestletterv4.doc",
	"www.rishikumar.com/uploads/3/3/0/6/3306532/cpuc_protestletterv5b.doc",
]

@task
def ping():
	urls = ['https://bruinscan.herokuapp.com', 'https://shivaum.herokuapp.com']
	urls += links
	for url in urls:
		time.sleep(10)
		driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
		driver.set_window_size(1804, 1096)
		driver.get(url)
		driver.quit()
	app.control.purge()


def text(phone_number, carrier_address, msg):
	print msg
	msg += "\n\nbruinscan . herokuapp . com\n"
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("bruinscan@gmail.com", BRUINSCAN_PASS)
	server.sendmail("bruinscan@gmail.com", phone_number +"@"+ carrier_address, msg) 
	server.quit()



# @periodic_task(run_every=(crontab(minute='*/1')), ignore_result=True)
@task
def scanner(username, phone_number, carrier_address, sections, course_name, term, url, status_dictionary):

	task_name = username+" "+course_name

	actual_course_name = course_name
	course_name = course_name.replace(":","")

	msg = "Scanning started for " + str(course_name)
	# text(phone_number, carrier_address, msg)

	sections_arg = sections

	sections = sections.split("\n")
	lectures = {}
	for item in sections:
		if ":" in item:
			lecture = item.split(": ")[0]
			sections = item.split(": ")[1].split("|*|")
			lectures[lecture] = sections
		elif item != "":
			lectures[item] = ""

	try:

		# driver = webdriver.Firefox()
		driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
		driver.set_window_size(1804, 1096)
		
		driver.get(url)

		while True:
			try:
				driver.find_element_by_css_selector("input[tabindex='1']")  
				break
			except:
				pass
		user = driver.find_element_by_css_selector("input[tabindex='1']")  
		password = driver.find_element_by_css_selector("input[tabindex='2']")

		user.send_keys(MYUCLA_USER)
		password.send_keys(MYUCLA_PASS)
		driver.find_element_by_css_selector("button[tabindex='3']").click()
		# time.sleep(3)

		status_dict = {}
		while True:
			try:
				status_dict = eval(Task_Data.objects.values_list('status_dict').get(task_name=task_name)[0])
				break
			except Task_Data.DoesNotExist:
				break
			except:
				print "***** WAITING FOR SQL SERVER ******"
				time.sleep(5)
				continue


		if not status_dict:
			for lec, discussions in lectures.iteritems():
				if not discussions:
					status_dict[lec] = "Closed"
				else:
					for disc in discussions:
						status_dict[lec+disc] = "Closed"
		else:
			for lec, discussions in lectures.iteritems():
				if not discussions:
					if not lec in status_dict:
						status_dict[lec] = "Closed"
				else:
					for disc in discussions:
						key = lec+disc
						if not key in status_dict:
							status_dict[key] = "Closed"


		hierarchy = ["Open", "Waitlist", "Closed"]

		while True:

			timeout = time.time() + 60 #one minute from now
			while True:
				try:
					if time.time() > timeout:
						print "error with expandall"
						driver.quit()
						return scanner(username, phone_number, carrier_address, sections_arg, actual_course_name, url, status_dict)
					driver.find_element_by_id("expandAll")
					break
				except:
					pass

			while True:
				try:
					for arrow in driver.find_elements_by_class_name('icon-caret-right'):
						before = len(driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:])
						arrow.click()
						while True:
							after = len(driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:])
							if after-before>0:
								break
					break
				except:
					print "caret Unexpected error:", sys.exc_info()[0]


			section_data = driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:]
			status_data = driver.find_elements_by_xpath("//div/div[@class='statusColumn']")[1:]

			sections = []
			for item in section_data:
				sections.append(item.text)

			statuses = []
			for item in status_data:
				statuses.append(item.text)

			courses_to_look_at = []

			if any(x in course_name for x in courses_to_look_at):
				print task_name
				print lectures
				print status_dict

			for lec, discussions in lectures.iteritems():

				if any(x in course_name for x in courses_to_look_at):
					print lec, discussions


				if not discussions:
					if lec in sections:
						index = sections.index(lec)
						status = statuses[index]
						# print lec + ": " + status
						if "Open" in status:
							if hierarchy.index(status_dict[lec]) > 0:
								msg = course_name + " " + lec + " open! - " + status.replace(":", "")
								text(phone_number, carrier_address, msg)
								status_dict[lec] = "Open"

						elif "Waitlist" in status:
							if hierarchy.index(status_dict[lec]) > 1:
								msg = course_name + " " + lec + " - waitlist spot is open " + status.replace(":", "")
								text(phone_number, carrier_address, msg)
								status_dict[lec] = "Waitlist"

						elif "Closed" in status:
							status_dict[lec] = "Closed"

						else:
							if "Left" in status:
								if hierarchy.index(status_dict[lec]) > 0:
									status_dict[lec] = "Open"
									msg = course_name + " " + lec + + " open!"
									text(phone_number, carrier_address, msg)
							elif "Taken" in status:
								if hierarchy.index(status_dict[lec]) > 1:
									status_dict[lec] = "Waitlist"
									msg = course_name + " " + lec + + " waitlist spot open"
									text(phone_number, carrier_address, msg)
							else:
								status_dict[lec] = "Closed"
							# print abbrev + " " + course_name + " WTF: " + status
					else:
						status_dict[lec] = "Closed"
						status = "Closed"
						# print lec + ": " + status

				else:
					if "Lec" in lec:
						possible = ["Lec", "Sem", "Tut", "Rgp", "Stu"]
					else:
						possible = ["Lec", "Lab", "Sem", "Tut", "Rgp", "Stu"]

					if lec not in sections:
						for disc in discussions:
							# print lec + " " + disc + ": " + "Closed"
							key = lec+disc
							status_dict[key] = "Closed"
						continue

					first = sections.index(lec)
					i = first + 1
					while i<len(sections) and not any (x in sections[i] for x in possible):
						i+=1
					last = i

					current_lectures = sections[first:last]
					current_statuses = statuses[first:last]

					for disc in discussions:
						if disc in current_lectures:
							index = current_lectures.index(disc)
							key = lec+disc
							status = current_statuses[index]
							# print lec + " " + disc + ": " + status
							if "Open" in status:
								if hierarchy.index(status_dict[key]) > 0:
									status_dict[key] = "Open"
									msg = course_name + " " + lec + " " + disc + " open! - " + status.replace(":", "")
									text(phone_number, carrier_address, msg)

							elif "Waitlist" in status:
								if hierarchy.index(status_dict[key]) > 1:
									status_dict[key] = "Waitlist"
									msg = course_name + " " + lec + " " + disc + " waitlist spot is open - " + status.replace(":", "")
									text(phone_number, carrier_address, msg)

							elif "Closed" in status:
								status_dict[key] = "Closed"

							else:
								if "Left" in status:
									if hierarchy.index(status_dict[key]) > 0:
										status_dict[key] = "Open"
										msg = course_name + " " + lec + " " + disc + " open!"
										text(phone_number, carrier_address, msg)
								elif "Taken" in status:
									if hierarchy.index(status_dict[key]) > 1:
										status_dict[key] = "Waitlist"
										msg = course_name + " " + lec + " " + disc + " waitlist spot open"
										text(phone_number, carrier_address, msg)
								else:
									status_dict[key] = "Closed"
								# print abbrev + " " + course_name + " WTF: " + status
						else:
							key = lec+disc
							status_dict[key] = "Closed"
							status = "Closed"
							# print lec + " " + disc + ": " + status


			# task = PeriodicTask.objects.get(name=task_name) # if we suppose names are unique
			# task.args=json.dumps([username, phone_number, carrier_address, sections, actual_course_name, subject_name, abbrev, url, status_dict])
			# task.save()

			Task_Data(task_name=task_name, status_dict=str(status_dict)).save()
			driver.quit()

			break # just run once

	except KeyboardInterrupt:
		driver.quit()
	except:
		driver.quit()
		print "problem with " + task_name 
		traceback.print_exc()



# scanner("Lec 1: Dis 1A, Dis 1B\n", "31 - Introduction to Computer Science I", "Computer Science", "COM SCI", "GEOG", "5165811305", "txt.att.net")
# scanner("Lec 1\n", "111 - Forest Ecosystems", "Geography", "GEOG", "5165811305", "txt.att.net")


@worker_ready.connect
def at_start(sender, **k):
	with sender.app.connection() as conn:
		# sender.app.send_task('scanner.tasks.populate', connection=conn)
		pass


@celeryd_init.connect()
def randomize_last_runs(sender=None, conf=None, **kwargs):

	print "****CELERY CONNECT****"

	# get_subject_data_chrome()

	app.control.purge()

	# 2017-03-28 04:00:00.006667+00:00

	schedule, created = IntervalSchedule.objects.get_or_create(every=frequency,period=IntervalSchedule.SECONDS,)
	i = datetime.now()

	tasks = PeriodicTask.objects.all()
	index = 0
	for task in tasks:
		if task.name in ["ping"]:
			continue
		time = round((frequency/len(tasks))*index, 3)
		past_time = i - timedelta(seconds=time)
		past_time = past_time.strftime('%Y-%m-%d %H:%M:%S.000000+00:00')
		print past_time
		task.interval = schedule
		task.last_run_at = past_time
		task.save()
		index += 1
	print index

@task
def update():

	phone_numbers, carriers = zip(*User.objects.values_list('phone_number', 'carrier_address').reverse())

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("bruinscan@gmail.com", BRUINSCAN_PASS)
	

	for phone_number, carrier in zip(phone_numbers[:6:-1], carriers[:6:-1]):
		try:
			print phone_number
			msg = "Scanning is up for Summer Sessions!"
			msg += "\n\nbruinscan dot herokuapp dot com\n"
			server.sendmail("bruinscan@gmail.com", phone_number +"@"+ carrier, msg) 
			time.sleep(10)
		except:
			print str(phone_number) + " didnt work"
			traceback.print_exc()

	server.quit()

	pass


@task
def bruinwalk():

	courses, all_instructors = zip(*Class_Data.objects.values_list('course', 'instructors'))

	keys = courses

	courses = [" ".join(x.split(" ")[1:]) for x in courses]
	courses = [x.split(" -")[0].lower().replace("&","-").replace(" ", "-") for x in courses]
	all_instructors = [x.split("|*|") for x in all_instructors]


	for key, course, instructor_list in zip(keys, courses, all_instructors):

		print key

		instructor_list = [x.split("\n") for x in instructor_list]
		instructor_list = [ [x.split(",")[0] for x in y] for y in instructor_list]

		url = "http://www.bruinwalk.com/classes/" + course

		distributions = []
		for instructors in instructor_list:
			max_perc, distribution = get_grades(url, instructors)
			if distribution=="COURSE NOT FOUND":
				print url
				distributions.append(str([]))
			elif distribution!=[]:
				distributions.append(str([max_perc] + distribution))
			else:
				distributions.append(str(distribution))

		obj = Class_Data.objects.get(course=key)
		obj.grades="|*|".join(distributions)
		obj.save()
			

@task
def prereqs():
	with open('data.csv', 'w') as file:
		file.write("abbreviation,")
		file.write("course,")
		file.write("requisites,")
		file.write("recommended,")
		file.write("\n")
	subjects = Class_Data.objects.values_list('subject').distinct().order_by('subject')
	for subject in subjects:
		subject = subject[0]
		if subject.rfind("(")>=0:
			abbrev = subject[subject.rfind("(")+1:subject.rfind(")")]
		else:
			abbrev = subject.upper()
		get_prereqs(abbrev)




@task
def populate():

	terms = []
	# terms.append("SummerSessionA")
	terms.append("SummerSessionC")

	for current_term in terms:

		subjects = get_subjects_courses(current_term)
		# subjects = collections.OrderedDict([(u'African American Studies (AF AMER)', [u'6 - Trends in Black Intellectual Thought', u'M150D - Recent African American Urban History: Funk Music and Politics of Black Popular Culture', u'188A - Soul, American Sociopolitical Culture, and Pursuit of Freedom', u'188A - Special Courses in Afro-American Studies']), (u'Ancient Near East (AN N EA)', [u'10W - Jerusalem: Holy City']), (u'Anthropology (ANTHRO)', [u'7 - Human Evolution', u'124B - Evolutionary Psychology', u'135S - Anthropology of Deviance and Abnormality', u'139 - Field Methods in Cultural Anthropology', u'147 - Human and Nonhuman Communication: Anthropological Perspectives on Language and Cross-Species Interaction', u'147 - Selected Topics in Linguistic Anthropology', u'149A - Language and Identity', u'M154Q - Gender Systems: Global', u'596 - Individual Studies for Graduate Students']), (u'Applied Linguistics (APPLING)', [u'30W - Language and Social Interaction', u'40W - Language and Gender: Introduction to Gender and Stereotypes', u'101W - Introduction to Language Learning and Language Teaching']), (u'Arabic', [u'M107 - Islam in West']), (u'Armenian (ARMENIA)', [u'120 - Language in Diaspora: Armenian as a Heritage Language']), (u'Art', [u'11B - Photography']), (u'Art History (ART HIS)', [u'C114D - Selected Topics in Ancient Art', u'130 - Selected Topics in Modern Art', u'154B - Later Art of India', u'156 - Arts of Southeast Asia', u'C169 - Designing Participatory Democracy', u'C169 - Selected Topics in Architectural History', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Asian', [u'M60W - Introduction to Buddhism']), (u'Asian American Studies (ASIA AM)', [u'30W - Asian American Literature and Culture', u'M114 - Asian American Education and Schooling', u'M129 - Health Issues for Asian Americans and Pacific Islanders: Myth or Model?', u'130A - Chinese American Experience', u'187B - Special Courses in Asian American Themes']), (u'Astronomy (ASTR)', [u'5 - Life in Universe']), (u'Atmospheric and Oceanic Sciences (A&O SCI)', [u'104 - Fundamentals of Air and Water Pollution']), (u'Bioengineering (BIOENGR)', [u'199 - Directed Research in Bioengineering']), (u'Biomedical Research (BMD RES)', [u'5HA - Biomedical Research: Concepts and Strategies']), (u'Biostatistics (BIOSTAT)', [u'100A - Introduction to Biostatistics', u'400 - Field Studies in Biostatistics']), (u'Chemistry and Biochemistry (CHEM)', [u'14B - Thermodynamics, Electrochemistry, Kinetics, and Organic Chemistry', u'14BL - General and Organic Chemistry Laboratory I', u'14CL - General and Organic Chemistry Laboratory II', u'17 - Chemical Principles', u'20B - Chemical Energetics and Change', u'30B - Organic Chemistry II: Reactivity, Synthesis, and Spectroscopy', u'30BL - Organic Chemistry Laboratory I', u'153A - Biochemistry: Introduction to Structure, Enzymes, and Metabolism', u'153B - Biochemistry: DNA, RNA, and Protein Synthesis', u'196A - Research Apprenticeship in Chemistry and Biochemistry', u'196B - Research Apprenticeship in Chemistry and Biochemistry', u'596 - Directed Individual Study or Research', u'598 - Research for and Preparation of M.S. Thesis', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Chicana and Chicano Studies (CHICANO)', [u'10B - Introduction to Chicana/Chicano Studies: Social Structure and Contemporary Conditions', u'CM106 - Health in Chicano/Latino Population', u'M108A - Music of Latin America: Mexico, Central America, and Caribbean Isles', u'M114 - Chicanos in Film/Video', u'151 - Human Rights in Americas', u'CM182 - Understanding Whiteness in American History and Culture', u'188 - Special Courses in Chicana and Chicano Studies', u'188 - Transfrontera: Introduction to U.S.-Mexico Transborder Studies']), (u'Civic Engagement (CIVIC)', [u'152 - Exploring Social Change: Critical Analysis through Lens of Community Organizing and Social Movements']), (u'Civil and Environmental Engineering (C&EE)', [u'102 - Dynamics of Particles and Bodies', u'108 - Introduction to Mechanics of Deformable Solids', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Classics (CLASSIC)', [u'10 - Discovering Greeks', u'30 - Classical Mythology', u'41W - Reading Roman Literature: Writing-Intensive']), (u'Communication Studies (COMM ST)', [u'1 - Principles of Oral Communication', u'1A - Public Speaking for Nonnative Speakers', u'1B - Learning American English and Culture from Movies', u'105 - Conspiracy Theories, Media, and Middle East', u'109 - Entrepreneurial Communication', u'110 - Gender and Communication', u'140 - Theory of Persuasive Communication', u'148 - Integrated Marketing Communications', u'M149 - Media: Gender, Race, Class, and Sexuality', u'156 - Social Networking', u'195 - Summer Internships']), (u'Community Health Sciences (COM HLT)', [u'48 - Nutrition and Food Studies: Principles and Practice', u'100 - Introduction to Community Health Sciences', u'M140 - Health Issues for Asian Americans and Pacific Islanders: Myth or Model?', u'400 - Field Studies in Public Health', u"597 - Preparation for Master's Comprehensive or Doctoral Qualifying Examinations"]), (u'Comparative Literature (COM LIT)', [u'4CW - Literature and Writing: Age of Enlightenment to 20th Century', u'4DW - Literature and Writing: Great Books from World at Large']), (u'Computer Science (COM SCI)', [u'596 - Directed Individual or Tutorial Studies']), (u'Dance', [u'11 - Beginning World Arts Practices in South Asia and Diaspora', u'11 - Beginning Yoga']), (u'Design / Media Arts (DESMA)', [u'8 - Media Histories', u'25 - Typography', u'160 - Special Topics in Design | Media Arts']), (u'Disability Studies (DIS STD)', [u'101W - Perspectives on Disability Studies', u'120 - Special Topics on Race and Disability', u'M125 - Exploring Intersections of Ability and Sexuality', u'M161 - Sports, Normativity, and Body']), (u'Earth, Planetary, and Space Sciences (EPS SCI)', [u'16 - Major Events in History of Life', u'599 - Ph.D. Research and Dissertation Preparation']), (u'Ecology and Evolutionary Biology (EE BIOL)', [u'111 - Biology of Vertebrates', u'120 - Evolution', u'129 - Animal Behavior', u'162 - Plant Physiology', u'193 - Journal Club Seminars: Ecology and Evolutionary Biology', u'194B - Research Group or Internship Seminars: Ecology and Evolutionary Biology']), (u'Economics (ECON)', [u'1 - Principles of Economics', u'2 - Principles of Economics', u'11 - Microeconomic Theory', u'41 - Statistics for Economists', u'97 - Economic Toolkit', u'101 - Microeconomic Theory', u'102 - Macroeconomic Theory', u'103 - Introduction to Econometrics', u'103L - Econometrics Laboratory', u'106F - Finance', u'122 - International Finance']), (u'Education (EDUC)', [u'M103 - Asian American Education and Schooling', u'M108 - Sociology of Education', u'133 - Topics in Child Development and Social Policies', u'196R - Research Apprenticeship in Education', u'596 - Directed Independent Study', u'599 - Dissertation Research']), (u'Electrical Engineering (EL ENGR)', [u'3 - Introduction to Electrical Engineering', u'597A - Preparation for M.S. Comprehensive Examination', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Engineering (ENGR)', [u'120 - Entrepreneurship for Scientists and Engineers', u'195 - Internship Studies in Engineering']), (u'English (ENGL)', [u'4W - Critical Reading and Writing', u'20W - Introduction to Creative Writing', u"M107A - Studies in Women's Writing", u'M107A - Women Writers and Fairy Tale Tradition', u'115E - Science Fiction', u'129 - Comic Fiction, or Graphic Novel', u'129 - Topics in Genre Studies, Interdisciplinary Studies, and Critical Theory', u'M138 - Life Skills: Art of Interview', u'M138 - Topics in Creative Writing', u'142 - Later Medieval Literature', u'163C - Jane Austen and Her Peers', u'174C - Contemporary American Fiction', u'174C - Narratives of Media, Technology, and Community', u'599 - Ph.D. Dissertation Research']), (u'English Composition (ENGCOMP)', [u'2 - Approaches to University Writing', u'3 - English Composition, Rhetoric, and Language', u'5W - Literature, Culture, and Critical Inquiry', u'131B - Specialized Writing: Business and Social Policy']), (u'English as A Second Language (ESL)', [u'20 - Conversation and Fluency', u'21 - Pronunciation', u'22 - Public Speaking', u'23 - American Culture through Film', u'24 - Preparation for American Universities', u'25 - Academic Reading and Writing', u'26 - Business Communication: Speaking', u'97A - English through Language, Culture, and Society: Sex, Gender, and Sexuality', u'97A - Variable Topics in English as a Second Language', u'105 - Advanced Grammar and Style for Multilingual Students']), (u'Environment (ENVIRON)', [u'M133 - Environmental Sociology']), (u'Epidemiology (EPIDEM)', [u'100 - Principles of Epidemiology', u"597 - Preparation for Master's Comprehensive or Doctoral Qualifying Examinations"]), (u'Ethnomusicology (ETHNMUS)', [u'50A - Jazz in American Culture: Late 19th Century through 1940s', u'M108A - Music of Latin America: Mexico, Central America, and Caribbean Isles', u'188 - Asian Pop', u'188 - Special Courses in Ethnomusicology']), (u'Family Medicine (FAM MED)', [u'199 - Directed Research in Family Medicine']), (u'Film and Television (FILM TV)', [u'33 - Introductory Screenwriting', u'84A - Overview of Contemporary Film Industry', u'114 - Film Genres', u'114 - Film Noir', u'M117 - Chicanos in Film/Video', u'122B - Introduction to Art and Technique of Filmmaking', u'122E - Digital Cinematography', u'122M - Film and Television Directing', u'C132 - Screenwriting Fundamentals', u'183C - Producing III: Marketing, Distribution, and Exhibition', u'194 - Internship Seminars: Film, Television, and Digital Media', u'195 - Corporate Internships in Film, Television, and Digital Media', u'498 - Professional Internship in Film and Television', u'596F - Directed Individual Studies: Production']), (u'Food Studies (FOOD ST)', [u'27 - Critical Thinking about Food and Science Publications']), (u'French (FRNCH)', [u'596 - Directed Individual Studies or Research', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Gender Studies (GENDER)', [u'104 - Bodies', u"M107A - Studies in Women's Writing", u'M136 - Music and Gender', u'M149 - Media: Gender, Race, Class, and Sexuality', u'M154Q - Gender Systems: Global', u'M161 - Sports, Normativity, and Body']), (u'Geography (GEOG)', [u'3 - Cultural Geography', u"5 - People and Earth's Ecosystems", u'7 - Introduction to Geographic Information Systems', u'116 - Biogeography of Plant and Animal Invasions', u'125 - Health and Global Environment', u'147 - Social Geography', u'168 - Intermediate Geographic Information Systems', u'184 - California', u'598 - Research for and Preparation of M.A. Thesis', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'German', [u'596 - Directed Individual Study or Research', u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Global Studies (GLBL ST)', [u'1 - Globalization: Markets', u"160 - Hollywood and America's Global Image", u'160 - Selected Topics in Global Studies']), (u'Health Policy and Management (HLT POL)', [u'225A - Health Services Research Design', u'596 - Directed Individual Study or Research']), (u'History (HIST)', [u'1C - Introduction to Western Civilization: Circa 1715 to Present', u'13C - History of the U.S. and Its Colonial Origins: 20th Century', u'121E - History of Modern Europe: Era of Total War, 1914 to 1945', u'M150D - Recent African American Urban History: Funk Music and Politics of Black Popular Culture', u'M151C - Understanding Whiteness in American History and Culture', u'154 - History of California', u'157B - Indians of Colonial Mexico', u'164D - Topics in African History: Africa and Diaspora in Global and Comparative Perspective', u'199 - Directed Research in History']), (u'Honors Collegium (HNRS)', [u'101A - Student Research Forum', u'199 - Directed Honors Studies']), (u'Information Studies (INF STD)', [u'599 - Ph.D. Research and Writing']), (u'International Development Studies (INTL DV)', [u'110 - Economic Development and Culture Change', u'130 - Economics of Developing Countries', u'191 - Education, Gender, and Social Inclusion: Policy and Practice', u'191 - Variable Topics Research Seminars: International Development Studies -- Senior Seminar']), (u'International and Area Studies (I A STD)', [u'33 - Introduction to East Asia', u'50 - Introduction to Latin America']), (u'Islamic Studies (ISLM ST)', [u'M107 - Islam in West']), (u'Italian', [u'2 - Elementary Italian -- Continued', u'596 - Directed Individual Studies', u'599 - Ph.D. Research and Writing']), (u'Japanese (JAPAN)', [u'70 - Images of Japan: Literature and Film', u'C159 - Race, Gender, and Class through Literature and Film', u'C159 - Variable Topics in Culture and Society in Japan']), (u'Korean (KOREA)', [u'50 - History of Korean Civilization', u'155 - Topics in Korean Cinema']), (u'Labor and Workplace Studies (LBR&WS)', [u'M149 - Media: Gender, Race, Class, and Sexuality', u'188 - Special Courses in Labor and Workplace Studies', u'188 - Working Class Narratives: History, Memory, and Immigrant Experience in Los Angeles', u'194A - Research Group Seminars: Labor Summer Research Internship Program', u'194A - Ride Sharing or Ride Stealing? Working Gig Economy in Los Angeles', u'195A - Community or Corporate Internships in Labor and Workplace Studies']), (u'Lesbian, Gay, Bisexual, Transgender, and Queer Studies (LGBTQS)', [u'M125 - Exploring Intersections of Ability and Sexuality', u'181 - Variable Topics in Queer Diversities']), (u'Life Sciences (LIFESCI)', [u'1 - Evolution, Ecology, and Biodiversity', u'2 - Cells, Tissues, and Organs', u'3 - Introduction to Molecular Biology', u'4 - Genetics', u'23L - Introduction to Laboratory and Scientific Methodology', u'192A - Undergraduate Practicum in Life Sciences', u'192B - Undergraduate Practicum in Life Sciences']), (u'Linguistics (LING)', [u'1 - Introduction to Study of Language', u'20 - Introduction to Linguistic Analysis', u'120A - Phonology I', u'120B - Syntax I', u'120C - Semantics I', u'170 - Language and Society: Introduction to Sociolinguistics']), (u'Management (MGMT)', [u'1B - Principles of Accounting', u'120B - Intermediate Financial Accounting II', u'127B - Corporate and Partnership Taxation', u'142B - Communication Technology, Programming, and Accounting', u'160 - Entrepreneurship and Venture Initiation', u'161 - Business Plan Development', u'163 - Entrepreneurship and New Product Development', u'180 - Business Interpersonal Communication', u'180 - Special Topics in Management', u'182 - Leadership Principles and Practice', u'195 - Community or Corporate Internships in Management', u'199 - Directed Research in Management']), (u'Mathematics (MATH)', [u'3B - Calculus for Life Sciences Students', u'31B - Integration and Infinite Series', u'32B - Calculus of Several Variables', u'33B - Differential Equations', u'95 - Transition to Upper Division Mathematics', u'115A - Linear Algebra', u'131A - Analysis', u'142 - Mathematical Modeling', u'170B - Probability Theory', u'175 - Introduction to Financial Mathematics', u'296G - Research Seminar: Analysis']), (u'Mechanical and Aerospace Engineering (MECH&AE)', [u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Medicine (MED)', [u'199 - Directed Research in Medicine']), (u'Molecular and Medical Pharmacology (M PHARM)', [u'599 - Research for and Preparation of Ph.D. Dissertation']), (u'Music (MUSC)', [u'80A - Beginning Keyboard', u'80F - Beginning Guitar Class', u'80V - Vocal Technique for Beginners', u'188 - Anatomy of Popular Song', u'188 - Introduction to Music Therapy', u'188 - Nationalism in Music during World Wars', u'188 - Special Courses in Music']), (u'Music History (MSC HST)', [u'12W - Writing about Music', u'60 - American Musical', u'64 - Motown and Soul: African American Popular Music of 1960s', u'70 - Beethoven', u'M136 - Music and Gender']), (u'Music Industry (MSC IND)', [u'101 - Seminar: Music Industry, Technology, and Science', u'107A - Audio Technology for Musicians I', u'111 - Musicianship through Repertoire in Studio', u'112 - Comprehensive Songwriting']), (u'Neuroscience (NEUROSC)', [u'M119L - Human Neuropsychology']), (u'Nursing', [u'3 - Human Physiology for Healthcare Providers', u'175 - Physical Assessment for Advanced Practice', u'199 - Directed Research or Senior Project in Nursing', u'204 - Research Design and Critique', u'227 - Ethnogeriatric Nursing', u'445 - Advanced Practice Nursing: Clinical Nurse Specialist Practicum', u'597 - Individual Study for Comprehensive Examination']), (u'Philosophy (PHILOS)', [u'3 - Historical Introduction to Philosophy', u'7 - Introduction to Philosophy of Mind', u'22 - Introduction to Ethical Theory', u'23 - Meaning and Communication', u'31 - Logic, First Course', u'116 - 19th-Century Philosophy', u'116 - Nietzsche', u'129 - Honeybees, Computation, and Concepts: Mental Representations in Psychology', u'129 - Philosophy of Psychology', u'151A - History of Ethics: Selected Classics in Ancient Ethical Theories -- Plato, Aristotle', u'155 - Ending, Creating, and Selecting for Life', u'155 - Medical Ethics', u'177A - Existentialism']), (u'Physics', [u'1A - Physics for Scientists and Engineers: Mechanics', u'1B - Physics for Scientists and Engineers: Oscillations, Waves, Electric and Magnetic Fields', u'1C - Physics for Scientists and Engineers: Electrodynamics, Optics, and Special Relativity', u'4AL - Physics Laboratory for Scientists and Engineers: Mechanics', u'4BL - Physics Laboratory for Scientists and Engineers: Electricity and Magnetism', u'6A - Physics for Life Sciences Majors: Mechanics', u'6B - Physics for Life Sciences Majors: Waves, Electricity, and Magnetism', u'6C - Physics for Life Sciences Majors: Light, Fluids, Thermodynamics, Modern Physics']), (u'Physics and Biology in Medicine (PBMED)', [u'596 - Research in Biomedical Physics']), (u'Physiological Science (PHYSCI)', [u'5 - Issues in Human Physiology: Diet and Exercise', u'13 - Introduction to Human Anatomy', u'153 - Dissection Anatomy', u'166 - Animal Physiology', u'167 - Physiology of Nutrition']), (u'Political Science (POL SCI)', [u'6 - Introduction to Data Analysis', u'10 - Introduction to Political Theory', u'20 - World Politics', u'40 - Introduction to American Politics', u'50 - Introduction to Comparative Politics', u'123A - International Law', u'139 - International Interventions: Political and Legal Responses to Crises, Crimes, and Atrocities', u'139 - Special Studies in International Relations', u'150 - Political Violence']), (u'Portuguese (PORTGSE)', [u'M35 - Spanish, Portuguese, and Nature of Language']), (u'Psychology (PSYCH)', [u'10 - Introductory Psychology', u'20A - MATLAB Programming for Behavioral Sciences', u'85 - Introduction to Cognitive Science', u'100A - Psychological Statistics', u'100B - Research Methods in Psychology', u'115 - Principles of Behavioral Neuroscience', u'116 - Behavioral Neuroscience Laboratory', u'M119L - Human Neuropsychology', u'120A - Cognitive Psychology', u'129E - Human Sexuality', u'129F - Clinical Psychology of Childhood and Adolescence', u'130 - Developmental Psychology', u'136A - Social Psychology Laboratory', u'175 - Community Psychology', u'188B - Neuroimaging and Psychopathology', u'188B - Organizational Psychology', u'188B - Special Courses in Psychology']), (u'Public Health (PUB HLT)', [u'M106 - Health in Chicano/Latino Population', u'150 - Contemporary Health Issues']), (u'Religion, Study of (RELIGN)', [u'M107 - Islam in West']), (u'Scandinavian (SCAND)', [u'50W - Introduction to Scandinavian Literatures and Cultures']), (u'Social Welfare (SOC WLF)', [u'401A - Practicum: Social Work', u'401B - Practicum: Social Work', u'401C - Practicum: Social Work']), (u'Society and Genetics (SOC GEN)', [u'5 - Integrative Approaches to Human Biology and Society', u'M133 - Environmental Sociology', u'134 - Food and Health in Global Perspective', u'188 - Bioart, Biohacking, and Citizen Science', u'188 - Special Courses in Society and Genetics']), (u'Sociology (SOCIOL)', [u'1 - Introductory Sociology', u'20 - Introduction to Sociological Research Methods', u'101 - Development of Sociological Theory', u'102 - Contemporary Sociological Theory', u'111 - Social Networks', u'M115 - Environmental Sociology', u'130 - Self and Society', u'134 - Culture and Personality', u'145 - Sociology of Deviant Behavior', u'173 - Economy and Society', u'M175 - Sociology of Education', u'182 - Political Sociology', u'295 - Working Group in Sociology']), (u'Spanish (SPAN)', [u'1 - Elementary Spanish', u'2 - Elementary Spanish', u'3 - Elementary Spanish', u'M35 - Spanish, Portuguese, and Nature of Language', u'44 - Latin American Culture', u'160 - Topics in Spanish Linguistics']), (u'Statistics (STATS)', [u'10 - Introduction to Statistical Reasoning', u'20 - Introduction to Statistical Programming with R', u'100A - Introduction to Probability', u'100B - Introduction to Mathematical Statistics', u'100C - Linear Models', u'102A - Introduction to Computational Statistics with R', u'596 - Directed Individual Study or Research']), (u'Theater', [u'10 - Introduction to Theater', u'20 - Acting Fundamentals', u'21 - Acting for Camera', u'30 - Dramatic Writing', u'107 - Drama of Diversity', u'120A - Acting and Performance in Film', u'120B - Acting and Performance in Film']), (u'Urban Planning (URBN PL)', [u'121 - Urban Policy and Planning', u'129 - Cultural Perspectives on Gentrification', u'129 - Special Topics in Urban Policy and Research', u'199 - Directed Research in Urban Planning', u'599 - Ph.D. Dissertation Research in Planning']), (u'World Arts and Cultures (WL ARTS)', [u'178 - Advanced Private Instruction in World Arts and Cultures', u'195 - Community or Corporate Internships in World Arts and Cultures'])])


		for subject, courses in subjects.iteritems():
			
			# get abbreviation
			abbrev = ""
			if subject[-1]!=")":
				abbrev = subject.upper()
			else:
				i = len(subject)-1
				while subject[i]!="(":
					i-=1
				abbrev = subject[i+1:-1]
			abbrev = abbrev.replace(" ","&") #no spaces to store in database

			# if subject in complete:
			# 	continue

			print subject

			i = 0
			for url, sections, statuses, day_times, locations, instructors in get_url_section_data(subject, courses, current_term):
				course = current_term + " " + abbrev + " " + courses[i]
				Class_Data(subject=subject, course=course, url=url, sections=sections, statuses=statuses, day_times=day_times, locations=locations, instructors=instructors).save()
				i+=1

		text("4086217236", "txt.att.net", "Updated database successfully for " + current_term)












