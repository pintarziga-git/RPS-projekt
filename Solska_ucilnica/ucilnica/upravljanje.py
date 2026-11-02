from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PredmetUrediForm, PreprostUporabnikForm
from .models import Predmet

# Do upravljanja sme samo administrator.
admin_only = user_passes_test(lambda user: user.is_authenticated and user.is_active and user.is_superuser, login_url='prijava')

@admin_only
def predmeti(request):
    iskanje = request.GET.get('q', '').strip()
    seznam = Predmet.objects.order_by('naziv')
    if iskanje:
        seznam = seznam.filter(naziv__icontains=iskanje)
    return render(request, 'upravljanje/predmeti.html', {'predmeti': seznam, 'q': iskanje})

@admin_only
def predmet_obrazec(request, pk=None):
    predmet = get_object_or_404(Predmet, pk=pk) if pk is not None else None
    obrazec = PredmetUrediForm(request.POST or None, instance=predmet)
    if request.method == 'POST' and obrazec.is_valid():
        obrazec.save()
        messages.success(request, 'Predmet je shranjen.')
        return redirect('upravljanje_predmeti')
    return render(request, 'upravljanje/predmet_obrazec.html', {'obrazec': obrazec, 'predmet': predmet})

@admin_only
@require_POST
def predmet_izbrisi(request, pk):
    predmet = get_object_or_404(Predmet, pk=pk)
    predmet.delete()
    messages.success(request, 'Predmet je izbrisan.')
    return redirect('upravljanje_predmeti')

@admin_only
def uporabniki(request):
    q = request.GET.get('q', '').strip()
    seznam = User.objects.filter(is_superuser=False, is_staff=False).prefetch_related('groups').order_by('last_name', 'first_name', 'username')
    if q:
        seznam = seznam.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    uporabniki = [{'uporabnik': u, 'vloga': 'Učitelj' if any(g.name == 'Ucitelj' for g in u.groups.all()) else 'Učenec'} for u in seznam]
    return render(request, 'upravljanje/uporabniki.html', {'uporabniki': uporabniki, 'q': q})

@admin_only
def uporabnik_obrazec(request, pk=None):
    uporabnik = get_object_or_404(User, pk=pk, is_superuser=False, is_staff=False) if pk is not None else None
    obrazec = PreprostUporabnikForm(request.POST or None, uporabnik=uporabnik)
    if request.method == 'POST' and obrazec.is_valid():
        obrazec.save()
        messages.success(request, 'Uporabnik je shranjen.')
        return redirect('upravljanje_uporabniki')
    return render(request, 'upravljanje/uporabnik_obrazec.html', {'obrazec': obrazec, 'uporabnik': uporabnik})

@admin_only
@require_POST
def uporabnik_izbrisi(request, pk):
    uporabnik = get_object_or_404(User, pk=pk, is_superuser=False, is_staff=False)
    uporabnik.delete()
    messages.success(request, 'Uporabnik je izbrisan.')
    return redirect('upravljanje_uporabniki')
