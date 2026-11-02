#!/usr/bin/env bash
# Za že delujočo Oracle različico, brez posodobitve Docker slike.
set -euo pipefail
cd "$HOME/solska-ucilnica/solska_ucilnica_koncna"
umask 077
IZVOZ="$HOME/testni_racuni.csv"
if [ -e "$IZVOZ" ]; then
  echo "Datoteka $IZVOZ že obstaja. Ne bom je prepisal." >&2
  exit 1
fi
trap 'rm -f "$IZVOZ"' ERR
sudo docker compose exec -T aplikacija python - <<'PY' > "$IZVOZ"
import os, io, csv, secrets, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth.models import User, Group
from django.db import transaction
from ucilnica.models import Predmet

nazivi = ['Matematika','Slovenščina','Angleščina','Fizika','Kemija',
          'Biologija','Zgodovina','Geografija','Informatika','Športna vzgoja']
izhod = io.StringIO()
pisec = csv.writer(izhod)
pisec.writerow(['uporabnisko_ime','vloga','geslo'])
novi_u = novi_d = preskoceni = 0
with transaction.atomic():
    ucitelj, _ = Group.objects.get_or_create(name='Ucitelj')
    ucenec, _ = Group.objects.get_or_create(name='Ucenec')
    predmeti = []
    for naziv in nazivi:
        p = Predmet.objects.filter(naziv=naziv).order_by('pk').first()
        predmeti.append(p if p else Predmet.objects.create(naziv=naziv))
    for i in range(1, 121):
        je_ucitelj = i <= 20
        n = i if je_ucitelj else i-20
        username = ('ucitelj' if je_ucitelj else 'ucenec') + str(n)
        if User.objects.filter(username__iexact=username).exists():
            preskoceni += 1
            continue
        geslo = secrets.token_urlsafe(18)
        u = User.objects.create_user(username=username, password=geslo,
            first_name='Testni',last_name=('Učitelj ' if je_ucitelj else 'Učenec ')+str(n))
        u.groups.add(ucitelj if je_ucitelj else ucenec)
        if je_ucitelj:
            predmeti[(n-1)%10].ucitelji.add(u)
            predmeti[(n+4)%10].ucitelji.add(u)
            novi_u += 1
        else:
            for z in (0,3,6):
                predmeti[(n-1+z)%10].ucenci.add(u)
            novi_d += 1
        pisec.writerow([username,'ucitelj' if je_ucitelj else 'ucenec',geslo])
sys.stdout.write(izhod.getvalue())
print(f'Ustvarjeno: {novi_u} uciteljev in {novi_d} ucencev. Obstojeci: {preskoceni}.',file=sys.stderr)
PY
chmod 600 "$IZVOZ"
trap - ERR
echo "Gesla so samo na Oracle strezniku v $IZVOZ. Ne nalagaj na GitHub!"
