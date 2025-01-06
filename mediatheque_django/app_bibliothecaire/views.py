import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from .models import Membre, Livre, DVD, CD, JeuDePlateau, Emprunt
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import Http404

logger = logging.getLogger('app_mediatheque')

#  Authentification 
def custom_logout(request):
    logout(request)
    return render(request, 'auth/logout.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            login(request, user)   
            return redirect('liste_emprunts')  
        else:
            return render(request, 'auth/login.html', {'form': form, 'error_message': 'Identifiants incorrects'})
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


# Gestion des membres 
@login_required
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'membres/liste_membres.html', {'membres': membres})

@login_required
def ajout_membre(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        if nom:
            Membre.objects.create(nom=nom)
            return redirect('liste_membres')
        
        return render(request, 'membres/creer_membre.html', {'error': 'Le nom est requis'})
    return render(request, 'membres/creer_membre.html')

@login_required
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, pk=membre_id)
    membre.delete()
    return redirect('liste_membres')

@login_required
def mettre_a_jour_membre(request, membre_id):
    membre = get_object_or_404(Membre, pk=membre_id)
    if request.method == 'POST':
        nouveau_nom = request.POST.get('nom')
        if nouveau_nom:
            membre.nom = nouveau_nom
            membre.save()
            return redirect('liste_membres')
    return render(request, 'membres/mettre_a_jour_membre.html', {'membre': membre})


# Gestion des médias
def liste_medias(request):
    
    livres = Livre.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    jeux = JeuDePlateau.objects.all()
    return render(request, 'medias/liste_medias.html', {
        'livres': livres,
        'dvds': dvds,
        'cds': cds,
        'jeux': jeux
    })

@login_required
def ajouter_media(request, media_type):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        if not nom:
            return render(request, 'medias/ajouter_media.html', {
                'media_type': media_type,
                'error': 'Le champ "Nom" est requis.'
            })

        
        if media_type == 'livre':
            auteur = request.POST.get('auteur')
            if not auteur:
                return render(request, 'medias/ajouter_media.html', {
                    'media_type': media_type,
                    'error': 'Le champ "Auteur" est requis.'
                })
            Livre.objects.create(nom=nom, auteur=auteur)
        elif media_type == 'dvd':
            realisateur = request.POST.get('realisateur')
            if not realisateur:
                return render(request, 'medias/ajouter_media.html', {
                    'media_type': media_type,
                    'error': 'Le champ "Réalisateur" est requis.'
                })
            DVD.objects.create(nom=nom, realisateur=realisateur)
        elif media_type == 'cd':
            artiste = request.POST.get('artiste')
            if not artiste:
                return render(request, 'medias/ajouter_media.html', {
                    'media_type': media_type,
                    'error': 'Le champ "Artiste" est requis.'
                })
            CD.objects.create(nom=nom, artiste=artiste)
        elif media_type == 'jeu':
            createur = request.POST.get('createur')
            if not createur:
                return render(request, 'medias/ajouter_media.html', {
                    'media_type': media_type,
                    'error': 'Le champ "Créateur" est requis.'
                })
            JeuDePlateau.objects.create(nom=nom, createur=createur)

        return redirect('liste_medias')

    return render(request, 'medias/ajouter_media.html', {'media_type': media_type})


@login_required
def supprimer_media(request, media_type, media_id):
    media_model = {
        'livre': Livre,
        'dvd': DVD,
        'cd': CD,
        'jeu': JeuDePlateau
    }.get(media_type)

    media = get_object_or_404(media_model, pk=media_id)


    emprunt_actif = Emprunt.objects.filter(
        content_type=ContentType.objects.get_for_model(media),
        object_id=media.id,
        date_retour__isnull=True
    ).exists()

    if emprunt_actif:
        messages.error(request, f"Le média '{media.nom}' est actuellement emprunté et ne peut pas être supprimé.")
        return redirect('liste_medias')

    media.delete()
    messages.success(request, f"Le média '{media.nom}' a été supprimé avec succès.")
    return redirect('liste_medias')


# Gestion des Emprunts
@login_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'emprunts/liste_emprunts.html', {
        'emprunts': emprunts,
        'now': timezone.now()
    })

@login_required
def emprunter_media(request):
    error_message = None

    if request.method == 'POST':

        membre_id = request.POST.get('membre_id')
        media_type = request.POST.get('media_type')
        media_id = request.POST.get('media_id')

        membre = get_object_or_404(Membre, pk=membre_id)
        
       
        media_model = {
            'livre': Livre,
            'dvd': DVD,
            'cd': CD,
        }.get(media_type.lower())

        if not media_model: 
            error_message = "Type de média invalide. Veuillez sélectionner un type valide."
        else:
            try:
                media = get_object_or_404(media_model, pk=media_id)

                if Emprunt.objects.filter(membre=membre, date_retour__isnull=True).count() >= 3:
                    error_message = "Ce membre a atteint la limite d'emprunts."
                elif not media.disponible:
                    error_message = f"Le média '{media.nom}' n'est pas disponible."
                else:
                    try:
                        emprunt = Emprunt(
                            membre=membre,
                            content_type=ContentType.objects.get_for_model(media),
                            object_id=media.id
                        )
                        emprunt.valider_emprunt()
                        return redirect('confirmation_emprunt')
                    except ValueError as e:
                        error_message = str(e)
            except Http404:
                error_message = f"Veuillez selectionner le bon type de média."

    
    return render(request, 'emprunts/emprunter_media.html', {
        'membres': Membre.objects.all(),
        'livres': Livre.objects.filter(disponible=True),
        'dvds': DVD.objects.filter(disponible=True),
        'cds': CD.objects.filter(disponible=True),
        'error_message': error_message,  
    })
@login_required
def retourner_media(request, emprunt_id):

    emprunt = get_object_or_404(Emprunt, pk=emprunt_id)
    emprunt.retourner_medias()
    return redirect('liste_emprunts')


@login_required
def confirmation_emprunt(request):
    return render(request, 'emprunts/confirmation_emprunt.html')

@login_required
def limite_emprunts(request):
    return render(request, 'emprunts/limite_emprunts.html')

