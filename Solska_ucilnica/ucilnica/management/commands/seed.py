from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from ucilnica.models import Predmet

PREDMETI = ['Matematika','Slovenščina','Angleščina','Fizika','Kemija',
           'Biologija','Zgodovina','Geografija','Informatika','Športna vzgoja']

class Command(BaseCommand):
    help = 'Ustvari osnovne predmete, brez testnih učiteljev in učencev.'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='Ucitelj')
        Group.objects.get_or_create(name='Ucenec')
        if not Predmet.objects.exists():
            for ime in PREDMETI:
                Predmet.objects.get_or_create(naziv=ime)
        self.stdout.write(self.style.SUCCESS('Predmeti so pripravljeni. Testnih uporabnikov ne ustvarjam.'))
