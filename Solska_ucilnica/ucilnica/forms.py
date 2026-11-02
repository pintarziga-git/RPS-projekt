from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gradivo, Predmet

RAZŠIRITVE={'.pdf','.doc','.docx','.ppt','.pptx','.txt','.jpg','.jpeg','.png','.odt','.xlsx','.zip'}
MAX_SIZE=15*1024*1024

def preveri_datoteko(datoteka):
    from pathlib import Path
    if datoteka.size > MAX_SIZE:
        raise forms.ValidationError('Datoteka je prevelika (največ 15 MB).')
    if Path(datoteka.name).suffix.lower() not in RAZŠIRITVE:
        raise forms.ValidationError('Dovoljene so datoteke PDF, Word, PowerPoint, slike, TXT, Excel in ZIP.')
    return datoteka

class Registracija(UserCreationForm):
    first_name=forms.CharField(label='Ime',max_length=150)
    last_name=forms.CharField(label='Priimek',max_length=150)
    class Meta:
        model=User
        fields=['username','first_name','last_name','password1','password2']
        labels={'username':'Uporabniško ime'}

class GradivoForm(forms.ModelForm):
    datoteka=forms.FileField(label='Datoteka',validators=[preveri_datoteko])
    class Meta:
        model=Gradivo
        fields=['naslov','datoteka']
        labels={'naslov':'Naslov gradiva'}

class NalogaForm(forms.Form):
    naslov=forms.CharField(label='Naslov naloge',max_length=150)
    datoteka=forms.FileField(label='Datoteka',validators=[preveri_datoteko])
    potrdi=forms.BooleanField(label='Potrjujem zamenjavo prejšnje oddaje z istim naslovom',required=False)

class ProfilForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
        labels={'first_name':'Ime','last_name':'Priimek','email':'E-pošta'}


# Preprosta obrazca za administratorja, brez zahtevnih Django admin polj.
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

class PredmetUrediForm(forms.ModelForm):
    class Meta:
        model = Predmet
        fields = ['naziv', 'ucitelji', 'ucenci']
        labels = {'naziv': 'Ime predmeta', 'ucitelji': 'Učitelji', 'ucenci': 'Učenci'}
        widgets = {
            'ucitelji': forms.CheckboxSelectMultiple,
            'ucenci': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ucitelji'].queryset = User.objects.filter(groups__name='Ucitelj',is_active=True).distinct().order_by('last_name','first_name','username')
        self.fields['ucenci'].queryset = User.objects.filter(groups__name='Ucenec',is_active=True).distinct().order_by('last_name','first_name','username')
        self.fields['ucitelji'].required = False
        self.fields['ucenci'].required = False

    def clean_naziv(self):
        from .models import Predmet
        naziv = self.cleaned_data['naziv'].strip()
        drugi = Predmet.objects.filter(naziv__iexact=naziv)
        if self.instance.pk:
            drugi = drugi.exclude(pk=self.instance.pk)
        if drugi.exists():
            raise ValidationError('Ta predmet že obstaja.')
        return naziv


class PreprostUporabnikForm(forms.Form):
    username = forms.CharField(label='Uporabniško ime', max_length=150)
    first_name = forms.CharField(label='Ime', max_length=150)
    last_name = forms.CharField(label='Priimek', max_length=150)
    email = forms.EmailField(label='E-pošta (neobvezno)', required=False)
    vloga = forms.ChoiceField(label='Vloga', choices=[('Ucenec','Učenec'),('Ucitelj','Učitelj')])
    geslo = forms.CharField(label='Geslo', widget=forms.PasswordInput, min_length=8, required=False,
                             help_text='Najmanj 8 znakov. Pri urejanju pusti prazno, če gesla ne spreminjaš.')

    def __init__(self, *args, uporabnik=None, **kwargs):
        self.uporabnik = uporabnik
        if uporabnik and (not args or args[0] is None) and 'initial' not in kwargs:
            kwargs['initial'] = {
                'username':uporabnik.username, 'first_name':uporabnik.first_name,
                'last_name':uporabnik.last_name, 'email':uporabnik.email,
                'vloga':'Ucitelj' if uporabnik.groups.filter(name='Ucitelj').exists() else 'Ucenec',
            }
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        exists = User.objects.filter(username__iexact=username)
        if self.uporabnik:
            exists = exists.exclude(pk=self.uporabnik.pk)
        if exists.exists():
            raise ValidationError('Uporabniško ime je že zasedeno.')
        return username

    def clean_geslo(self):
        geslo = self.cleaned_data.get('geslo')
        if not self.uporabnik and not geslo:
            raise ValidationError('Vnesi geslo za novega uporabnika.')
        if geslo:
            from django.contrib.auth.password_validation import validate_password
            validate_password(geslo, user=self.uporabnik)
        return geslo

    def save(self):
        from .models import Predmet
        data = self.cleaned_data
        uporabnik = self.uporabnik or User()
        prejsnja_vloga = 'Ucitelj' if (self.uporabnik and self.uporabnik.groups.filter(name='Ucitelj').exists()) else 'Ucenec'
        uporabnik.username = data['username']
        uporabnik.first_name = data['first_name'].strip()
        uporabnik.last_name = data['last_name'].strip()
        uporabnik.email = data['email']
        if data['geslo']:
            uporabnik.set_password(data['geslo'])
        uporabnik.save()
        if self.uporabnik and prejsnja_vloga != data['vloga']:
            if prejsnja_vloga == 'Ucitelj':
                for predmet in Predmet.objects.filter(ucitelji=uporabnik):
                    predmet.ucitelji.remove(uporabnik)
            else:
                for predmet in Predmet.objects.filter(ucenci=uporabnik):
                    predmet.ucenci.remove(uporabnik)
        skupina, _ = Group.objects.get_or_create(name=data['vloga'])
        skupine = list(Group.objects.filter(name__in=['Ucitelj','Ucenec']))
        uporabnik.groups.remove(*skupine)
        uporabnik.groups.add(skupina)
        return uporabnik
