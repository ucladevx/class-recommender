from django.core.management.base import BaseCommand
from scanner.models import Home_Data, Course_Data, Section_Data
from classes import *
import sys

class Command(BaseCommand):
    help = 'populate or clean database'

    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Remove all items from table',
        )

    def add_data(self):
    	Home_Data.objects.all().delete()

    	print "Getting majors..."
    	subjects, names, abbrevs = get_data()
    	for subject, name, abbrev in zip(subjects, names, abbrevs):
    		Home_Data(subject=subject, subject_name=name, abbrev=abbrev).save()

    	Course_Data.objects.all().delete()
        Section_Data.objects.all().delete()

        names = names[6:]
        abbrevs = abbrevs[6:]

    	print "Getting courses and discussion for each major. Takes about 1 hour..."
    	for name, abbrev in zip(names, abbrevs):

            print name

            courses, sections, statuses, waitlists = get_course_and_section_data(name, abbrev)
            # courses is a string separated by |*|
            try:
                Course_Data(abbrev=abbrev, courses=courses).save()
            except:
                print "Course Unexpected error:", sys.exc_info()[0]

            courses = courses.split("|*|")  # need a list of courses to iterate through

            for course, section, status, waitlist in zip(courses, sections, statuses, waitlists):
                try:
                    Section_Data(course=course, sections=section, statuses=status, waitlists=waitlist).save()
                except:
                    print "Section Unexpected error:", sys.exc_info()[0]
    	


    def handle(self, *args, **options):
    	if options['clean']:
    		Home_Data.objects.all().delete()
    		Course_Data.objects.all().delete()
    	else:
        	self.add_data()
