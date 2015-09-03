from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Prints all models and objects count in each of them'

    def handle(self, *args, **options):
        pass
