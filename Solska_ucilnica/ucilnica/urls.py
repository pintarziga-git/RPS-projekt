from django.urls import path
from django.contrib.auth import views as auth
from . import views, upravljanje

urlpatterns=[
    path('upravljanje/predmeti/',upravljanje.predmeti,name='upravljanje_predmeti'),
    path('upravljanje/predmeti/dodaj/',upravljanje.predmet_obrazec,name='upravljanje_predmet_dodaj'),
    path('upravljanje/predmeti/<int:pk>/uredi/',upravljanje.predmet_obrazec,name='upravljanje_predmet_uredi'),
    path('upravljanje/predmeti/<int:pk>/izbrisi/',upravljanje.predmet_izbrisi,name='upravljanje_predmet_izbrisi'),
    path('upravljanje/uporabniki/',upravljanje.uporabniki,name='upravljanje_uporabniki'),
    path('upravljanje/uporabniki/dodaj/',upravljanje.uporabnik_obrazec,name='upravljanje_uporabnik_dodaj'),
    path('upravljanje/uporabniki/<int:pk>/uredi/',upravljanje.uporabnik_obrazec,name='upravljanje_uporabnik_uredi'),
    path('upravljanje/uporabniki/<int:pk>/izbrisi/',upravljanje.uporabnik_izbrisi,name='upravljanje_uporabnik_izbrisi'),
    path('',views.domov,name='domov'),
    path('prijava/',auth.LoginView.as_view(template_name='prijava.html',redirect_authenticated_user=True),name='prijava'),
    path('odjava/',auth.LogoutView.as_view(),name='odjava'),
    path('registracija/',views.registracija,name='registracija'),
    path('predmet/<int:pk>/',views.predmet,name='predmet'),
    path('gradivo/<int:pk>/prenos/',views.gradivo_prenos,name='gradivo_prenos'),
    path('naloga/<int:pk>/prenos/',views.naloga_prenos,name='naloga_prenos'),
    path('gradivo/<int:pk>/brisi/',views.brisi_gradivo,name='brisi_gradivo'),
    path('profil/',views.profil,name='profil'),
    path('moji-predmeti/',views.moji_predmeti,name='moji_predmeti'),
]
