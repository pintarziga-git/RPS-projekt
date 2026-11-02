import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='Ustvari lokalnega demo administratorja, če še ne obstaja.'
    def handle(self,*args,**kwargs):
        ime=os.getenv('DEMO_ADMIN_USERNAME','admin')
        geslo=os.getenv('DEMO_ADMIN_PASSWORD')
        if not geslo:
            self.stdout.write('Brez DEMO_ADMIN_PASSWORD: preskočim demo administratorja.')
            return
        if User.objects.filter(username=ime).exists():
            self.stdout.write('Administrator že obstaja, ne spreminjam gesla.')
            return
        User.objects.create_superuser(ime,'',geslo)
        self.stdout.write(self.style.SUCCESS('Demo administrator je ustvarjen.'))
