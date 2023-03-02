from django.core.management.base import BaseCommand
from ...functions import get_all_urls_data


class Command(BaseCommand):
    help = 'Stahnuti aktualnich dat z CrUX API'

    def handle(self, *args, **options):
        get_all_urls_data()
        print('Úspěšně staženo')
        return