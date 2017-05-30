from django.core.management.base import BaseCommand
from scanner.classes import *
from scanner.tasks import populate, update, bruinwalk, prereqs

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


    def handle(self, *args, **options):
        prereqs()


