import urllib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sys, os
import time
from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.keys import Keys
import traceback
import collections

from scanner.globals import MYUCLA_USER, MYUCLA_PASS, BRUINSCAN_PASS, frequency




def get_subjects_courses(current_term):

	# Assuming term is either SummerSessionA and SummerSessionC
	session = ""
	if "Summer" in current_term:
		if "C" in current_term:
			session = "Session C"
		elif "A" in current_term:
			session = "Session A"
		search = "Summer"

	try:

		url = 'https://sa.ucla.edu/ro/ClassSearch'

		chromedriver = "/Users/Rishub/Desktop/Python/Selenium/chromedriver"	
		driver = webdriver.Chrome(chromedriver)
		driver.set_window_size(1280, 800)
		
		driver.get(url)

		username = driver.find_element_by_css_selector("input[tabindex='1']")  
		password = driver.find_element_by_css_selector("input[tabindex='2']")

		username.send_keys(MYUCLA_USER)
		password.send_keys(MYUCLA_PASS)
		driver.find_element_by_css_selector("button[tabindex='3']").click()

		term = driver.find_element_by_id("optSelectTerm")
		term = driver.find_element_by_id("optSelectTerm")

		term.send_keys(search)

		if search == "Summer":
			look_for = "select_summer_session"
		else:
			look_for = "select_filter_subject"

		while True:
			try:
				driver.find_element_by_id(look_for)
				time.sleep(1)
				break
			except KeyboardInterrupt:
				driver.quit()
				break
			except:
				pass

		while True:
			try:
				driver.find_element_by_id(look_for)
				break
			except KeyboardInterrupt:
				driver.quit()
				break
			except:
				pass


		if search=="Summer":
			summer = driver.find_element_by_id(look_for)
			summer.send_keys(session)
			while True:
				try:
					driver.find_element_by_id("select_filter_subject")
					time.sleep(3)
					break
				except:
					pass


		subjects = {}
		subject_index = 0

		subject_input = driver.find_element_by_id("select_filter_subject")
		subject_input.click()

		while True:

			if subject_index==0:
				subject_input.send_keys(Keys.UP)
				subject_input.send_keys(Keys.DOWN)
				subject_index=1
			else:
				subject_input.send_keys(Keys.DOWN)
			
			subject = driver.find_element_by_id("select_filter_subject").get_attribute('value')
			if subject:
				subjects[subject] = []
			else:
				break

		
		subjects = collections.OrderedDict(sorted(subjects.items()))

		for subject, courses in subjects.iteritems():

			subject_input = driver.find_element_by_id("select_filter_subject")
			subject_input.click()

			before = driver.find_element_by_xpath("//div[@id='div_subject']/span").text
			subject_input.send_keys(subject)
			while driver.find_element_by_xpath("//div[@id='div_subject']/span").text==before:
				pass
			subject_input.send_keys(Keys.RETURN)

			while True:
				try:
					driver.find_element_by_id("select_filter_catalog").send_keys("")
					break
				except:
					pass

			course_input = driver.find_element_by_id("select_filter_catalog")
			course_input.click()

			courses = []
			urls = []

			course_index=0
			while True:

				if course_index==0:
					course_input.send_keys(Keys.ARROW_UP)
					course_input.send_keys(Keys.ARROW_DOWN)
					course_index+=1
				else:
					course_input.send_keys(Keys.ARROW_DOWN)
					course_index+=1

				course = driver.find_element_by_id("select_filter_catalog").get_attribute('value')
				if course:
					courses.append(course)
				else:
					break

			subjects[subject] = courses

		driver.quit()

		return subjects

	except:
		driver.quit()
		traceback.print_exc()


def get_url_section_data(subject, courses, current_term):
	
	# Assuming term is either SummerSessionA and SummerSessionC
	session = ""
	search = ""
	if "Summer" in current_term:
		if "C" in current_term:
			session = "Session C"
		elif "A" in current_term:
			session = "Session A"
		search = "Summer"

	try:
		url = 'https://sa.ucla.edu/ro/ClassSearch'

		chromedriver = "/Users/Rishub/Desktop/Python/Selenium/chromedriver"	
		driver = webdriver.Chrome(chromedriver)
		driver.set_window_size(1804, 1096)
		
		driver.get(url)

		username = driver.find_element_by_css_selector("input[tabindex='1']")  
		password = driver.find_element_by_css_selector("input[tabindex='2']")

		username.send_keys(MYUCLA_USER)
		password.send_keys(MYUCLA_PASS)
		driver.find_element_by_css_selector("button[tabindex='3']").click()

		term = driver.find_element_by_id("optSelectTerm")
		term = driver.find_element_by_id("optSelectTerm")

		term.send_keys(search)

		if search == "Summer":
			look_for = "select_summer_session"
		else:
			look_for = "select_filter_subject"

		timeout = time.time() + 15
		while True:
			try:
				if time.time() > timeout:
					print "timed out1"
					driver.quit()
					return get_url_section_data(subject, courses, current_term)
				driver.find_element_by_id(look_for)
				time.sleep(1)
				break
			except KeyboardInterrupt:
				driver.quit()
				break
			except:
				pass

		timeout = time.time() + 15
		while True:
			try:
				if time.time() > timeout:
					print "timed out2"
					driver.quit()
					return get_url_section_data(subject, courses, current_term)
				driver.find_element_by_id(look_for)
				break
			except KeyboardInterrupt:
				driver.quit()
				break
			except:
				pass


		if search=="Summer":
			summer = driver.find_element_by_id(look_for)
			summer.send_keys(session)
			timeout = time.time() + 15
			while True:
				try:
					if time.time() > timeout:
						print "timed out3"
						driver.quit()
						return get_url_section_data(subject, courses, current_term)
					driver.find_element_by_id("select_filter_subject")
					time.sleep(2)
					break
				except KeyboardInterrupt:
					driver.quit()
					break
				except:
					pass


		urls = []
		sections = []
		statuses = []
		day_times = []
		locations = []
		instructors = []

		for course in courses:
			subject_input = driver.find_element_by_id("select_filter_subject")
			subject_input.click()
			before = driver.find_element_by_xpath("//div[@id='div_subject']/span").text
			subject_input.send_keys(subject)
			while driver.find_element_by_xpath("//div[@id='div_subject']/span").text==before:
				pass
			subject_input.send_keys(Keys.RETURN)

			while True:
				try:
					driver.find_element_by_id("select_filter_catalog").send_keys("")
					break
				except:
					pass

			course_input = driver.find_element_by_id("select_filter_catalog")
			course_input.send_keys(course)
			timeout = time.time() + 3
			while driver.find_element_by_xpath("//div[@id='div_catalog']/span").text[0:2] not in ["1 "]:
				if time.time() > timeout:
					break
			course_input.send_keys(Keys.RETURN)
			course_input.send_keys(Keys.RETURN)

			for arrow in driver.find_elements_by_class_name('icon-caret-right'):
				before = len(driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:])
				arrow.click()
				while True:
					after = len(driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:])
					if after-before>0:
						break

			urls.append(driver.current_url)

			section_data = driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")[1:]
			status_data = driver.find_elements_by_xpath("//div/div[@class='statusColumn']")[1:]
			day_data = driver.find_elements_by_xpath("//div/div[contains(@class, 'dayColumn')]")[1:]
			hour_data = driver.find_elements_by_xpath("//div/div[@class='timeColumn']")[1:]
			location_data = driver.find_elements_by_xpath("//div/div[@class='locationColumn ']")[1:]
			instructor_data = driver.find_elements_by_xpath("//div/div[@class='instructorColumn ']")[1:]

			# if len(section_data)==0:
				# print subject + " " + course + " multiple classes????"

			sections.append("|*|".join([item.text for item in section_data]))
			statuses.append("|*|".join([" ".join(item.text.split("\n")) for item in status_data]))
			day_times.append("|*|".join([day.text + " " + hour.text for day, hour in zip(day_data, hour_data)]))
			locations.append("|*|".join([item.text for item in location_data]))
			instructors.append("|*|".join([" ".join(item.text.split("\n")) for item in instructor_data]))

			driver.get(url)

		driver.quit()

		return zip(urls, sections, statuses, day_times, locations, instructors)

	except KeyboardInterrupt:
		driver.quit()

	except:
		driver.quit()
		traceback.print_exc()
		return get_url_section_data(subject, courses, current_term)



# chromedriver = "/Users/Rishub/Desktop/Python/Selenium/chromedriver"	
# driver = webdriver.Chrome(chromedriver)
# driver.set_window_size(1804, 1096)
# driver.get("http://www.google.com")

def get_grades(url, instructor_list):

	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	if soup.find_all("div", { "class": "errorCode row" }):
		return 0, "COURSE NOT FOUND"	# COURSE NOT FOUND

	for link in soup.find_all("a"):
		for instructor in instructor_list:
			prof = link.find_all("span", {"class": "prof name"})
			if not prof:
				continue
			if instructor in prof[0].text.split(" "):
				url = "http://www.bruinwalk.com" + link['href']

	if not url:
		return 0, []	# PROF NOT FOUND

	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	display = soup.find_all("div", { "class" : "dist-display" })
	if not display:
		return 0, []	# GRADES NOT FOUND
	
	display = display[0]

	term = display.find_all("h5")[0].text.strip()
	max_perc = float(display.find_all("span", { "class": "y-label" })[0].text.strip()[:-1])
	grades = [x.text.strip() for x in display.find_all("span", {"class": "x-label"})]

	distribution = []
	for item in display.find_all("div", { "class": "bar-fill"}):
		distribution.append(round(float(item['style'].split("height: ")[1][:-2])*float(max_perc)/100,3))


	return max_perc, distribution


import csv
def get_prereqs(abbrev):

	# There are five different categories of requisites: 
	# requisites, enforced requisites, corequisites, preparation, and recommended.

	url  = "http://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA={0}&funsel=3".format(abbrev)

	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	divs = soup.find_all("div", { "class": "media-body" })

	with open('data.csv', 'a') as file:
		for div in divs:
			print abbrev
			print div.h3.text
			file.write('"' + abbrev.encode('utf-8') + '",')
			file.write('"' + div.h3.text.encode('utf-8') + '",')
			description = div.find_all("p")[1].text
			requisites = ""
			recommended = ""
			for line in description.split(". "):
				if any(x in line.lower() for x in ["requisites: ", "requisite: "]):
					print line
					requisites = ": ".join(line.split(": ")[1:])
				if any(x in line.lower() for x in ["recommended preparation: ", "recommended: "]):
					print line
					recommended = ": ".join(line.split(": ")[1:])
			file.write('"' + requisites.encode('utf-8') + '",')
			file.write('"' + recommended.encode('utf-8') + '"')
			file.write("\n")


	# time.sleep(10)









