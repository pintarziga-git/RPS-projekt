import re
from pathlib import Path
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Count
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import GradivoForm, NalogaForm, ProfilForm, Registracija
from .models import Gradivo, Naloga, Predmet
from .roles import je_admin, je_ucitelj, sme_videti_predmet, sme_urejati_gradiva


def registracija(request):
    if request.user.is_authenticated:
        return redirect('domov')
    form=Registracija(request.POST or None)
    if request.method=='POST' and form.is_valid():
        uporabnik=form.save()
        skupina,_=Group.objects.get_or_create(name='Ucenec')
        uporabnik.groups.add(skupina)
        messages.success(request,'Račun je ustvarjen. Zdaj se lahko prijaviš.')
        return redirect('prijava')
    return render(request,'registracija.html',{'form':form})


def moji_predmeti_qs(user):
    if je_admin(user):
        return Predmet.objects.all()
    if je_ucitelj(user):
        return Predmet.objects.filter(ucitelji=user)
    return Predmet.objects.filter(ucenci=user)


@login_required
def domov(request):
    predmeti=moji_predmeti_qs(request.user).distinct().order_by('naziv')
    if je_admin(request.user):
        st_gradiv=Gradivo.objects.count()
        st_nalog=Naloga.objects.count()
    else:
        st_gradiv=Gradivo.objects.filter(predmet__in=predmeti).count()
        oddaje=Naloga.objects.filter(predmet__in=predmeti)
        st_nalog=oddaje.count() if je_ucitelj(request.user) else oddaje.filter(ucenec=request.user).count()
    return render(request,'domov.html',{
        'predmeti':predmeti,'st_predmetov':predmeti.count(),
        'st_gradiv':st_gradiv,'st_nalog':st_nalog,
        'je_admin':je_admin(request.user), 'je_ucitelj':je_ucitelj(request.user),
    })


def safe_ime(vrednost):
    s=re.sub(r'[\\/:*?"<>|\x00-\x1f]','',vrednost).strip().strip('.')
    return re.sub(r'\s+',' ',s)[:90] or 'Neznano'


@login_required
def predmet(request,pk):
    p=get_object_or_404(Predmet,pk=pk)
    if not sme_videti_predmet(request.user,p):
        return HttpResponseForbidden('Za ta predmet nimaš pravice dostopa.')
    upravlja=sme_urejati_gradiva(request.user,p)
    admin=je_admin(request.user)
    gf=GradivoForm(prefix='g')
    nf=NalogaForm(prefix='n')
    if request.method=='POST':
        if 'dodaj_gradivo' in request.POST:
            if not upravlja: return HttpResponseForbidden('Nimaš dovoljenja za nalaganje gradiv.')
            gf=GradivoForm(request.POST,request.FILES,prefix='g')
            if gf.is_valid():
                obj=gf.save(commit=False)
                obj.predmet=p
                obj.save()
                messages.success(request,'Gradivo je uspešno dodano.')
                return redirect('predmet',pk=p.pk)
        elif 'oddaj_nalogo' in request.POST:
            if admin or je_ucitelj(request.user): return HttpResponseForbidden('Naloge lahko oddajajo samo učenci.')
            nf=NalogaForm(request.POST,request.FILES,prefix='n')
            if nf.is_valid():
                naslov=nf.cleaned_data['naslov'].strip()
                predhodna=Naloga.objects.filter(predmet=p,ucenec=request.user,naslov=naslov).first()
                if predhodna and not nf.cleaned_data['potrdi']:
                    nf.add_error('potrdi','Nalogo s tem naslovom si že oddal. Za zamenjavo označi potrditveno polje.')
                else:
                    datoteka=nf.cleaned_data['datoteka']
                    podaljsek=Path(datoteka.name).suffix.lower()
                    ime=f"{safe_ime(request.user.last_name or request.user.username)} {safe_ime(request.user.first_name or request.user.username)} – {safe_ime(naslov)}{podaljsek}"
                    with transaction.atomic():
                        if predhodna:
                            # Enak naslov + isti učenec + predmet: nadomesti staro oddajo šele po potrditvi.
                            stara=predhodna.datoteka.name
                            predhodna.datoteka.save(ime,datoteka,save=True)
                            if stara!=predhodna.datoteka.name:
                                predhodna.datoteka.storage.delete(stara)
                        else:
                            nova=Naloga(predmet=p,ucenec=request.user,naslov=naslov)
                            nova.datoteka.save(ime,datoteka,save=True)
                    messages.success(request,'Naloga je uspešno oddana.')
                    return redirect('predmet',pk=p.pk)
        else:
            return HttpResponseForbidden('Neznana operacija.')
    gradiva=p.gradivo_set.select_related('predmet').order_by('-id')
    naloge=(p.naloga_set.select_related('ucenec').order_by('-id') if upravlja else
            p.naloga_set.filter(ucenec=request.user).order_by('-id'))
    return render(request,'predmet.html',{'p':p,'gradiva':gradiva,'naloge':naloge,
        'upravlja':upravlja,'je_ucenec':not upravlja,'gf':gf,'nf':nf})


@login_required
def gradivo_prenos(request,pk):
    g=get_object_or_404(Gradivo.objects.select_related('predmet'),pk=pk)
    if not sme_videti_predmet(request.user,g.predmet): return HttpResponseForbidden('Dostop zavrnjen.')
    try: return FileResponse(g.datoteka.open('rb'),as_attachment=True,filename=Path(g.datoteka.name).name)
    except FileNotFoundError: raise Http404('Datoteka ni najdena.')


@login_required
def naloga_prenos(request,pk):
    n=get_object_or_404(Naloga.objects.select_related('predmet','ucenec'),pk=pk)
    if not (je_admin(request.user) or request.user==n.ucenec or
            (je_ucitelj(request.user) and n.predmet.ucitelji.filter(pk=request.user.pk).exists())):
        return HttpResponseForbidden('Dostop zavrnjen.')
    try: return FileResponse(n.datoteka.open('rb'),as_attachment=True,filename=Path(n.datoteka.name).name)
    except FileNotFoundError: raise Http404('Datoteka ni najdena.')


@login_required
@require_POST
def brisi_gradivo(request,pk):
    g=get_object_or_404(Gradivo.objects.select_related('predmet'),pk=pk)
    if not sme_urejati_gradiva(request.user,g.predmet):
        return HttpResponseForbidden('Ni dovoljenja za brisanje.')
    predmet_id=g.predmet_id
    datoteka=g.datoteka.name
    g.delete()
    if datoteka: g.datoteka.storage.delete(datoteka)
    messages.success(request,'Gradivo je izbrisano.')
    return redirect('predmet',pk=predmet_id)


@login_required
def profil(request):
    form=ProfilForm(request.POST or None,instance=request.user)
    if request.method=='POST' and form.is_valid():
        form.save()
        messages.success(request,'Podatki so shranjeni.')
        return redirect('profil')
    return render(request,'profil.html',{'form':form})


@login_required
def moji_predmeti(request):
    if je_admin(request.user) or je_ucitelj(request.user):
        return HttpResponseForbidden('Seznam predmetov lahko spreminjajo samo učenci.')
    vsi=Predmet.objects.order_by('naziv')
    if request.method=='POST':
        ids=request.POST.getlist('predmeti')
        izbrani=vsi.filter(pk__in=ids)
        if izbrani.count()<2:
            messages.error(request,'Izberi vsaj dva predmeta.')
        else:
            request.user.obiskuje.set(izbrani)
            messages.success(request,'Predmeti so shranjeni.')
            return redirect('domov')
    izbrani_ids=list(request.user.obiskuje.values_list('pk',flat=True))
    return render(request,'moji_predmeti.html',{'predmeti':vsi,'izbrani':izbrani_ids})
