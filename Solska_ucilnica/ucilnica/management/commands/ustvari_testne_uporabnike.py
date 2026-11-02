from __future__ import annotations

import csv
import io
import secrets
import sys

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ucilnica.models import Predmet


PREDMETI = [
    'Matematika', 'Slovenščina', 'Angleščina', 'Fizika', 'Kemija',
    'Biologija', 'Zgodovina', 'Geografija', 'Informatika', 'Športna vzgoja',
]


class Command(BaseCommand):
    help = 'Ustvari 20 izmišljenih učiteljev in 100 izmišljenih učencev. Ne spreminja obstoječih računov.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--izvozi-gesla', action='store_true',
            help='Potrdi izpis CSV z novimi naključnimi gesli (shrani ga zasebno).',
        )

    def handle(self, *args, **options):
        if not options['izvozi_gesla']:
            raise CommandError('Manjka --izvozi-gesla. Izpis preusmeri v zaščiten CSV na računalniku.')

        izvoz = io.StringIO()
        csv_pisec = csv.writer(izvoz)
        csv_pisec.writerow(['uporabnisko_ime', 'vloga', 'geslo'])
        stevilo_uciteljev = 0
        stevilo_ucencev = 0
        preskoceni = 0

        with transaction.atomic():
            skupina_ucitelj, _ = Group.objects.get_or_create(name='Ucitelj')
            skupina_ucenec, _ = Group.objects.get_or_create(name='Ucenec')
            predmeti = []
            for naziv in PREDMETI:
                predmet = Predmet.objects.filter(naziv=naziv).order_by('id').first()
                if predmet is None:
                    predmet = Predmet.objects.create(naziv=naziv)
                predmeti.append(predmet)

            for i in range(1, 21):
                uporabnisko_ime = f'ucitelj{i}'
                if User.objects.filter(username__iexact=uporabnisko_ime).exists():
                    preskoceni += 1
                    continue
                geslo = secrets.token_urlsafe(18)
                uporabnik = User.objects.create_user(
                    username=uporabnisko_ime, password=geslo,
                    first_name='Testni', last_name=f'Učitelj {i}',
                )
                uporabnik.groups.add(skupina_ucitelj)
                # Vsak učitelj ima dva predmeta; skupaj 4 učitelji na predmet.
                predmeti[(i - 1) % 10].ucitelji.add(uporabnik)
                predmeti[(i + 4) % 10].ucitelji.add(uporabnik)
                csv_pisec.writerow([uporabnisko_ime, 'ucitelj', geslo])
                stevilo_uciteljev += 1

            for i in range(1, 101):
                uporabnisko_ime = f'ucenec{i}'
                if User.objects.filter(username__iexact=uporabnisko_ime).exists():
                    preskoceni += 1
                    continue
                geslo = secrets.token_urlsafe(18)
                uporabnik = User.objects.create_user(
                    username=uporabnisko_ime, password=geslo,
                    first_name='Testni', last_name=f'Učenec {i}',
                )
                uporabnik.groups.add(skupina_ucenec)
                # Vsak učenec ima tri predmete; skupaj 30 učencev na predmet.
                for zamik in (0, 3, 6):
                    predmeti[(i - 1 + zamik) % 10].ucenci.add(uporabnik)
                csv_pisec.writerow([uporabnisko_ime, 'ucenec', geslo])
                stevilo_ucencev += 1

        self.stdout.write(izvoz.getvalue(), ending='')
        self.stderr.write(
            f'Ustvarjeno: {stevilo_uciteljev} učiteljev in '
            f'{stevilo_ucencev} učencev. Že obstoječi računi: {preskoceni} (brez sprememb).'
        )
        self.stderr.write('CSV vsebuje gesla samo za novo ustvarjene račune. Hrani ga zasebno.')
