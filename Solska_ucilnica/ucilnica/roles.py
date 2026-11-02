def vloga(user):
    if not user.is_authenticated:
        return 'Gost'
    if user.is_superuser or user.is_staff:
        return 'Administrator'
    if user.groups.filter(name='Ucitelj').exists():
        return 'Učitelj'
    return 'Učenec'

def je_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

def je_ucitelj(user):
    return user.is_authenticated and user.groups.filter(name='Ucitelj').exists() and not je_admin(user)

def sme_videti_predmet(user, predmet):
    if not user.is_authenticated:
        return False
    if je_admin(user):
        return True
    if je_ucitelj(user):
        return predmet.ucitelji.filter(pk=user.pk).exists()
    return predmet.ucenci.filter(pk=user.pk).exists()

def sme_urejati_gradiva(user, predmet):
    return je_admin(user) or (je_ucitelj(user) and predmet.ucitelji.filter(pk=user.pk).exists())
