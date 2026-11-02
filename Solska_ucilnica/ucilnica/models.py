from django.db import models
from django.contrib.auth.models import User
from .storage import naloge_storage


class Predmet(models.Model):
    naziv=models.CharField(max_length=100)
    ucitelji=models.ManyToManyField(User,related_name='poucuje',blank=True)
    ucenci=models.ManyToManyField(User,related_name='obiskuje',blank=True)
    def __str__(self): return self.naziv
    class Meta:
        verbose_name='predmet';verbose_name_plural='Predmeti'


class Gradivo(models.Model):
    predmet=models.ForeignKey(Predmet,on_delete=models.CASCADE)
    naslov=models.CharField(max_length=150)
    datoteka=models.FileField(upload_to='gradiva/')
    def __str__(self): return self.naslov
    class Meta:
        verbose_name='gradivo';verbose_name_plural='Gradiva'


def pot_naloge(instance, ime):
    return f'naloge/{instance.predmet_id}/{instance.ucenec_id}/{ime}'


class Naloga(models.Model):
    predmet=models.ForeignKey(Predmet,on_delete=models.CASCADE)
    ucenec=models.ForeignKey(User,on_delete=models.CASCADE)
    naslov=models.CharField(max_length=150)
    datoteka=models.FileField(upload_to=pot_naloge,storage=naloge_storage)
    def __str__(self): return f'{self.naslov} ({self.ucenec})'
    class Meta:
        verbose_name='naloga';verbose_name_plural='Naloge'
        constraints=[models.UniqueConstraint(fields=['predmet','ucenec','naslov'],name='ena_oddaja')]
