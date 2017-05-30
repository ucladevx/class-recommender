import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import time
from selenium.common.exceptions import NoSuchElementException

def get_data():

	web = urllib.urlopen("https://sa.ucla.edu/ro/Public/SOC/")
	soup = BeautifulSoup(web.read().decode('utf-8'))
	scripts  = soup.find_all("script")
	data = ""
	for script in scripts:
		if 'subject' in script.text:
			data = script.text
	data = data.split("subjects")[1][5:].strip()
	data = data[:len(data)-3]

	classes = []
	for item in data.split(';'):
		if '(' in item:
			classes.append(item.replace('\u0026', '&').split('&quot')[0])

	names = []
	abbrev = []
	subjects = []
	for item in classes:
		temp = item.split('(')
		names.append(temp[0].strip())

		if len(temp)>2:
			abbrev.append(temp[2].split(')')[0])
		else:
			abbrev.append(temp[1].split(')')[0])	

		subjects.append(temp[0].strip() + ' (' + temp[1].split(')')[0] + ')')

	url_names = []
	url_abbrevs = []
	for i in range(0,len(names)):
		url_names.append(names[i].replace(' ', '+').replace(',', '%2C') + '+')
		url_abbrevs.append(abbrev[i].replace(' ', '+').replace('&', '%26'))

	return subjects, url_names, url_abbrevs

# def get_courses(url_name, url_abbrev):

# 	url = 'https://sa.ucla.edu/ro/Public/SOC/Results?t=17S&sBy=subject&sName={0}%28A{1}%29&subj={2}&crsCatlg=Enter+a+Catalog+Number+or+Class+Title+%28Optional%29&catlg=&cls_no=&btnIsInIndex=btn_inIndex/'.format(url_name, url_abbrev, url_abbrev)
# 	# driver = webdriver.Firefox()
# 	driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
# 	driver.get(url)
# 	courses=[]
# 	for course in driver.find_elements_by_css_selector('h3'):
# 		courses.append(course.text)
# 	try:
# 		i = 2
# 		while True:
# 			driver.find_element_by_link_text(str(i)).click()
# 			time.sleep(2)
# 			for course in driver.find_elements_by_css_selector('h3'):
# 				courses.append(course.text)
# 			i+=1
# 	except:
# 		pass

# 	return courses


def get_course_and_section_data(url_name, url_abbrev):

	# url = "https://sa.ucla.edu/ro/Public/SOC/Results?t=17S&sBy=subject&sName=Computer+Science+%28COM+SCI%29&subj=COM+SCI&crsCatlg=Enter+a+Catalog+Number+or+Class+Title+%28Optional%29&catlg=&cls_no=&btnIsInIndex=btn_inIndex&btnIsExchange=False"
	url = 'https://sa.ucla.edu/ro/Public/SOC/Results?t=17S&sBy=subject&sName={0}%28A{1}%29&subj={2}&crsCatlg=Enter+a+Catalog+Number+or+Class+Title+%28Optional%29&catlg=&cls_no=&btnIsInIndex=btn_inIndex/'.format(url_name, url_abbrev, url_abbrev)
	# driver = webdriver.Firefox()
	driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
	driver.get(url)

	courses = []
	sections = []
	statuses = []
	waitlists = []

	try:
		i = 1
		while True:
			if i!=1:
				driver.find_element_by_link_text(str(i)).click()
				time.sleep(2)

			driver.find_element_by_id('expandAll').click()
			time.sleep(10)

			for arrow in driver.find_elements_by_class_name('icon-caret-right'):
				arrow.click()

			course_data = driver.find_elements_by_css_selector('h3')
			for item in course_data:
				courses.append(item.text)
			
			
			section_data = driver.find_elements_by_xpath("//div/div[@class='sectionColumn']")
			current = []
			for item in section_data:
				if item.text == "Sect": #Section in Firefox? no one knows why
					if current:
						sections.append("|*|".join(current))
						current = []
					continue
				current.append(item.text)
			sections.append("|*|".join(current))


			status_data = driver.find_elements_by_xpath("//div/div[@class='statusColumn']")
			current = []
			for item in status_data:
				if item.text == "Status":
					if current:
						statuses.append("|*|".join(current))
						current = []
					continue
				current.append(", ".join(item.text.split("\n")))
			statuses.append("|*|".join(current))


			waitlist_data = driver.find_elements_by_xpath("//div/div[@class='waitlistColumn']")
			current = []
			for item in waitlist_data:
				if item.text == "Waitlist Status":
					if current:
						waitlists.append("|*|".join(current))
						current = []
					continue
				current.append(item.text)
			waitlists.append("|*|".join(current))

			i+=1
	except NoSuchElementException:
		pass

	courses = "|*|".join(courses)
	return courses, sections, statuses, waitlists



