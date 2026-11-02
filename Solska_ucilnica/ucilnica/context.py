from .roles import vloga

def uporabniska_vloga(request):
    return {'vloga': vloga(request.user)}
