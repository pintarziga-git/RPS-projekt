from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from .models import Predmet, Gradivo, Naloga

admin.site.site_header = 'Šolska učilnica – administracija'
admin.site.site_title = 'Šolska učilnica'
admin.site.index_title = 'Upravljanje podatkov'
admin.site.enable_nav_sidebar = False

@admin.register(Predmet)
class PredmetAdmin(admin.ModelAdmin):
    list_display = ('naziv',)
    search_fields = ('naziv',)

    def changelist_view(self, request, extra_context=None):
        return redirect('upravljanje_predmeti')

    def add_view(self, request, form_url='', extra_context=None):
        return redirect('upravljanje_predmet_dodaj')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return redirect('upravljanje_predmet_uredi', pk=object_id)

admin.site.unregister(User)
@admin.register(User)
class UporabnikAdmin(DefaultUserAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('upravljanje_uporabniki')

    def add_view(self, request, form_url='', extra_context=None):
        return redirect('upravljanje_uporabnik_dodaj')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Administratorja še vedno lahko urejamo v običajni Django administraciji.
        uporabnik = User.objects.filter(pk=object_id).first()
        if uporabnik and (uporabnik.is_superuser or uporabnik.is_staff):
            return super().change_view(request, object_id, form_url, extra_context)
        return redirect('upravljanje_uporabnik_uredi', pk=object_id)

@admin.register(Gradivo)
class GradivoAdmin(admin.ModelAdmin):
    list_display = ('naslov','predmet')
    list_filter = ('predmet',)
    search_fields = ('naslov',)

@admin.register(Naloga)
class NalogaAdmin(admin.ModelAdmin):
    list_display = ('naslov','predmet','ucenec')
    list_filter = ('predmet',)
    search_fields = ('naslov','ucenec__username','ucenec__first_name','ucenec__last_name')
