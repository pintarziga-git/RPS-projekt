from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

class Command(BaseCommand):
    help = 'Odstrani učence in učitelje. Vse administratorje ohrani. Zahteva --potrdi.'

    def add_arguments(self, parser):
        parser.add_argument('--potrdi', action='store_true', help='Resnično izbriši račune.')

    def handle(self, *args, **options):
        # Samo navadni uporabniki: admins (is_staff ali is_superuser) ostanejo.
        uporabniki = User.objects.filter(is_staff=False, is_superuser=False)
        st = uporabniki.count()
        if not options['potrdi']:
            self.stdout.write(f'Za brisanje je izbranih {st} neadministratorskih uporabnikov. Ponavljaj z --potrdi.')
            return
        with transaction.atomic():
            uporabniki.delete()
        self.stdout.write(self.style.SUCCESS(f'Izbrisanih {st} učencev/učiteljev. Administratorski računi ostanejo.'))
