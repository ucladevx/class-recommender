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
from scanner.password import PWD, PWD4
# from password import PWD, PWD4

def text(phone_number, carrier_address, msg):
	print msg
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("shivaum7@gmail.com", PWD4)
	server.sendmail("shivaum7@gmail.com", phone_number +"@"+ carrier_address, msg) 
	server.quit()

@task
def texting(username, phone_number, carrier_address, sections, course_name, subject_name, abbrev):
	print username
	print phone_number
	print carrier_address
	print sections
	print course_name
	print subject_name
	print abbrev
	msg = "Testing..."
	text(phone_number, carrier_address, msg)
	while True:
		time.sleep(60)
		msg = "still working for " + username + " " + course_name
		text(phone_number, carrier_address, msg)
		


# @periodic_task(run_every=(crontab(minute='*/1')), ignore_result=True)
@task
def scanner(username, phone_number, carrier_address, sections, course_name, subject_name, abbrev):

	msg = "Scanning started for " + str(abbrev) + " " + str(course_name)
	text(phone_number, carrier_address, msg)

	print course_name + ", " + sections + ", " + subject_name + "|*|" + abbrev

	sections = sections.split("\n")
	lectures = {}
	for item in sections:
		if ":" in item:
			lecture = item.split(": ")[0]
			sections = item.split(": ")[1].split(", ")
			lectures[lecture] = sections
		elif item != "":
			lectures[item] = ""
	print lectures

	url = 'https://sa.ucla.edu/ro/ClassSearch'
	# driver = webdriver.Firefox()
	driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
	driver.set_window_size(1804, 1096)
	driver.get(url)

	username = driver.find_element_by_css_selector("input[tabindex='1']")  
	password = driver.find_element_by_css_selector("input[tabindex='2']")

	username.send_keys("rishub")
	password.send_keys(PWD)
	driver.find_element_by_css_selector("button[tabindex='3']").click()

	try:
		time.sleep(5)
		term = driver.find_element_by_id("optSelectTerm")
		term.click()
		term.send_keys("Spring")
		term.send_keys(Keys.RETURN)
		time.sleep(5)

		subject = driver.find_element_by_id("select_filter_subject")
		subject.click()
		subject.send_keys(subject_name) 
		time.sleep(5)
		subject.send_keys('\n')
		time.sleep(5)

		driver.save_screenshot('screenshot1.png')

		course = driver.find_element_by_id("select_filter_catalog")
		course.click()
		driver.save_screenshot('screenshot2.png')
		course.send_keys(course_name)
		driver.save_screenshot('screenshot3.png')
		time.sleep(5)
		course.send_keys('\n')
		course.send_keys('\n')
		driver.save_screenshot('screenshot4.png')
		time.sleep(5)
	except:
		driver.save_screenshot('screenshot_last.png')
		print "saved screenshot"
		driver.close()
		sys.exit(0)



	hierarchy = ["Open", "Waitlist", "Closed"]
	status_dict = {}

	for lec, discussions in lectures.iteritems():
		if not discussions:
			status_dict[lec] = ""
		else:
			for disc in discussions:
				status_dict[lec+disc] = ""

	while True:

		while True:
			try:
				driver.find_element_by_id("expandAll")
				break
			except:
				pass

		for arrow in driver.find_elements_by_class_name('icon-caret-right'):
				arrow.click()

		section_data = driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:]
		status_data = driver.find_elements_by_xpath("//div/div[@class='statusColumn']")[1:]

		sections = []
		for item in section_data:
			sections.append(item.text)

		statuses = []
		for item in status_data:
			statuses.append(item.text)

		for lec, discussions in lectures.iteritems():
			if not discussions:
				index = sections.index(lec)
				status = statuses[index]
				print status
				if "Open" in status:
					if status_dict[lec]=="" or hierarchy.index(status_dict[lec]) > 0:
						msg = abbrev + " " + course_name + " open! - " + status.replace(":", "")
						text(phone_number, carrier_address, msg)
						status_dict[lec] = "Open"

				elif "Waitlist" in status:
					if status_dict[lec]=="" or hierarchy.index(status_dict[lec]) > 1:
						msg = abbrev + " " + course_name + " - waitlist spot is open " + status.replace(":", "")
						text(phone_number, carrier_address, msg)
						status_dict[lec] = "Waitlist"

				elif "Closed" in status:
					status_dict[lec] = "Closed"

				else:
					print "WTF: " + status


			else:
				if "Lec" in lec:
					possible = ["Lec", "Sem", "Tut"]
				else:
					possible = ["Lec", "Lab", "Sem", "Tut"]

				first = sections.index(lec)
				i = first
				while i<len(sections) and not any (x in sections[i] for x in possible):
					i+=1
				last = i - 1

				current_lectures = sections[first:last]
				current_statuses = statuses[first:last]
				for disc in discussions:
					if disc in current_lectures:
						index = current_lectures.index(disc)
						key = lec+disc
						status = current_statuses[index]
						print status
						if "Open" in status:
							if status_dict[key]=="" or hierarchy.index(status_dict[key]) > 0:
								msg = abbrev + " " + course_name + " open! - " + status.replace(":", "")
								text(phone_number, carrier_address, msg)
								status_dict[key] = "Open"

						elif "Waitlist" in status:
							if status_dict[key]=="" or hierarchy.index(status_dict[key]) > 1:
								msg = abbrev + " " + course_name + " - waitlist spot is open " + status.replace(":", "")
								text(phone_number, carrier_address, msg)
								status_dict[key] = "Waitlist"

						elif "Closed" in status:
							status_dict[key] = "Closed"

						else:
							print "WTF: " + status

		time.sleep(3)
		driver.refresh()



# scanner("Lec 1: Dis 1A, Dis 1B\n", "31 - Introduction to Computer Science I", "Computer Science", "COM SCI", "GEOG", "5165811305", "txt.att.net")
# scanner("Lec 1\n", "111 - Forest Ecosystems", "Geography", "GEOG", "5165811305", "txt.att.net")




















