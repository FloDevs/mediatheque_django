from django.shortcuts import render
from app_bibliothecaire.models import Livre, DVD, CD, JeuDePlateau

def liste_medias_membre(request):

    livres = Livre.objects.filter(disponible=True)
    dvds = DVD.objects.filter(disponible=True)
    cds = CD.objects.filter(disponible=True)
    jeux = JeuDePlateau.objects.all()  
    
    return render(request, 'liste_medias_membre.html', {
        'livres': livres,
        'dvds': dvds,
        'cds': cds,
        'jeux': jeux
    })
