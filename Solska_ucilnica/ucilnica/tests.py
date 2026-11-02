import tempfile
from pathlib import Path
from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Predmet, Gradivo, Naloga


class SolskaUcilnicaTests(TestCase):
    def setUp(self):
        self.teacher_group=Group.objects.create(name='Ucitelj')
        self.student_group=Group.objects.create(name='Ucenec')
        self.teacher=User.objects.create_user('ucitelj','ucitelj@example.com','geslo-123',first_name='Ana',last_name='Novak')
        self.teacher.groups.add(self.teacher_group)
        self.teacher2=User.objects.create_user('drugi','drugi@example.com','geslo-123')
        self.teacher2.groups.add(self.teacher_group)
        self.student=User.objects.create_user('ucenec','ucenec@example.com','geslo-123',first_name='Janez',last_name='Kos')
        self.student.groups.add(self.student_group)
        self.student2=User.objects.create_user('ucenec2','ucenec2@example.com','geslo-123')
        self.student2.groups.add(self.student_group)
        self.admin=User.objects.create_superuser('administrator','adm@example.com','geslo-123')
        self.math=Predmet.objects.create(naziv='Matematika')
        self.eng=Predmet.objects.create(naziv='Angleščina')
        self.math.ucitelji.add(self.teacher)
        self.math.ucenci.add(self.student)
        self.eng.ucitelji.add(self.teacher2)
        self.eng.ucenci.add(self.student2)
        self.temp=tempfile.TemporaryDirectory()
        self.media_override=override_settings(MEDIA_ROOT=self.temp.name)
        self.media_override.enable()

    def tearDown(self):
        self.media_override.disable()
        self.temp.cleanup()

    def datoteka(self,ime='naloga.pdf'):
        return SimpleUploadedFile(ime,b'%PDF-1.4\npreizkus',content_type='application/pdf')

    def test_ucitelj_vidi_samo_svoje_predmete(self):
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(reverse('predmet',args=[self.math.pk])).status_code,200)
        self.assertEqual(self.client.get(reverse('predmet',args=[self.eng.pk])).status_code,403)
        r=self.client.get(reverse('domov'))
        self.assertContains(r,'Matematika')
        self.assertNotContains(r,'Angleščina')

    def test_ucenec_ne_more_dodati_gradiva(self):
        self.client.force_login(self.student)
        r=self.client.post(reverse('predmet',args=[self.math.pk]),{
            'dodaj_gradivo':'1','g-naslov':'Skrivno','g-datoteka':self.datoteka()})
        self.assertEqual(r.status_code,403)
        self.assertEqual(Gradivo.objects.count(),0)

    def test_ucitelj_lahko_doda_in_brise_gradivo(self):
        self.client.force_login(self.teacher)
        r=self.client.post(reverse('predmet',args=[self.math.pk]),{
            'dodaj_gradivo':'1','g-naslov':'Razlaga','g-datoteka':self.datoteka('razlaga.pdf')})
        self.assertEqual(r.status_code,302)
        gradivo=Gradivo.objects.get()
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse('gradivo_prenos',args=[gradivo.pk])).status_code,200)
        self.client.force_login(self.teacher2)
        self.assertEqual(self.client.get(reverse('gradivo_prenos',args=[gradivo.pk])).status_code,403)
        self.client.force_login(self.teacher)
        r=self.client.post(reverse('brisi_gradivo',args=[gradivo.pk]))
        self.assertEqual(r.status_code,302)
        self.assertEqual(Gradivo.objects.count(),0)

    def test_ucenec_oddaja_in_zamenjava_s_potrditvijo(self):
        self.client.force_login(self.student)
        url=reverse('predmet',args=[self.math.pk])
        p={'oddaj_nalogo':'1','n-naslov':'Vaja 1','n-datoteka':self.datoteka()}
        self.assertEqual(self.client.post(url,p).status_code,302)
        naloga=Naloga.objects.get()
        self.assertIn('Kos Janez',naloga.datoteka.name)
        self.assertIn('Vaja 1',naloga.datoteka.name)
        self.assertEqual(self.client.post(url,{'oddaj_nalogo':'1','n-naslov':'Vaja 1','n-datoteka':self.datoteka()}).status_code,200)
        self.assertEqual(Naloga.objects.count(),1)
        self.assertEqual(self.client.post(url,{'oddaj_nalogo':'1','n-naslov':'Vaja 1','n-datoteka':self.datoteka(),'n-potrdi':'on'}).status_code,302)
        self.assertEqual(Naloga.objects.count(),1)

    def test_ucenec_ne_vidi_oddaje_drugega(self):
        self.client.force_login(self.student)
        self.client.post(reverse('predmet',args=[self.math.pk]),{
            'oddaj_nalogo':'1','n-naslov':'Test','n-datoteka':self.datoteka()})
        naloga=Naloga.objects.get()
        self.client.force_login(self.student2)
        self.assertEqual(self.client.get(reverse('naloga_prenos',args=[naloga.pk])).status_code,403)
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('naloga_prenos',args=[naloga.pk])).status_code,200)

    def test_zaklenjene_strani_in_registracija(self):
        self.assertEqual(self.client.get(reverse('domov')).status_code,302)
        r=self.client.post(reverse('registracija'),{
            'username':'nov_ucenec','first_name':'Miha','last_name':'Kranjc',
            'password1':'ZeloMocnoGeslo2026!','password2':'ZeloMocnoGeslo2026!'})
        self.assertEqual(r.status_code,302)
        self.assertTrue(User.objects.filter(username='nov_ucenec').exists())


class UpravljanjePreprostoTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin2', 'admin2@test.si', 'Geslo2026!')
        self.navaden = User.objects.create_user('u1','', 'Geslo2026!')
        self.navaden.groups.add(Group.objects.get_or_create(name='Ucenec')[0])

    def test_samo_admin_upravlja(self):
        self.client.force_login(self.navaden)
        self.assertNotEqual(self.client.get(reverse('upravljanje_uporabniki')).status_code, 200)
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('upravljanje_uporabniki')).status_code, 200)

    def test_dodaj_ucenca_in_ucitelja(self):
        self.client.force_login(self.admin)
        for i, vloga in enumerate(('Ucenec', 'Ucitelj')):
            r = self.client.post(reverse('upravljanje_uporabnik_dodaj'), {
                'username':f'nov{i}', 'first_name':'Nina', 'last_name':'Novak',
                'email':'', 'vloga':vloga, 'geslo':'Geslo2026!'} )
            self.assertEqual(r.status_code, 302)
            self.assertTrue(User.objects.get(username=f'nov{i}').groups.filter(name=vloga).exists())

    def test_predmet_urejanje(self):
        self.client.force_login(self.admin)
        p = Predmet.objects.create(naziv='Testni')
        r = self.client.post(reverse('upravljanje_predmet_uredi',args=[p.pk]),
                             {'naziv':'Tehnika','ucitelji':[],'ucenci':[]})
        self.assertEqual(r.status_code, 302)
        p.refresh_from_db()
        self.assertEqual(p.naziv, 'Tehnika')

    def test_admin_ostane_po_ciscenju(self):
        from django.core.management import call_command
        call_command('pocisti_uporabnike', '--potrdi')
        self.assertTrue(User.objects.filter(pk=self.admin.pk).exists())
        self.assertFalse(User.objects.filter(pk=self.navaden.pk).exists())


class TestniUporabnikiCommandTests(TestCase):
    def test_ustvarjanje_120_uporabnikov_brez_podvajanja(self):
        from io import StringIO
        from django.core.management import call_command

        izhod = StringIO()
        call_command('ustvari_testne_uporabnike', '--izvozi-gesla', stdout=izhod)
        self.assertEqual(User.objects.filter(groups__name='Ucitelj').count(), 20)
        self.assertEqual(User.objects.filter(groups__name='Ucenec').count(), 100)
        self.assertEqual(Predmet.objects.count(), 10)
        self.assertEqual(Predmet.objects.get(naziv='Matematika').ucitelji.count(), 4)
        self.assertEqual(Predmet.objects.get(naziv='Matematika').ucenci.count(), 30)
        self.assertTrue(User.objects.get(username='ucitelj1').check_password(
            izhod.getvalue().splitlines()[1].split(',')[-1]))
        drugic = StringIO()
        call_command('ustvari_testne_uporabnike', '--izvozi-gesla', stdout=drugic)
        self.assertEqual(User.objects.count(), 120)
        self.assertEqual(len(drugic.getvalue().splitlines()), 1)
