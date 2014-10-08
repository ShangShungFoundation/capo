from django.core.management.base import BaseCommand

from capo.capo import Capo


class Command(BaseCommand):
    help = 'Runs next available job'

    def handle(self, *args, **options):
        capo = Capo()
        run = capo.run_next_job()
