from django.urls import path
from . import views

urlpatterns = [
    # --- Authentification ---
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),

    # --- Gestion des membres ---
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/ajouter/', views.ajout_membre, name='ajout_membre'),
    path('membres/<int:membre_id>/supprimer/', views.supprimer_membre, name='supprimer_membre'),
    path('membres/<int:membre_id>/mettre-a-jour/', views.mettre_a_jour_membre, name='mettre_a_jour_membre'),

    # --- Gestion des médias ---
    path('medias/', views.liste_medias, name='liste_medias'),
    path('medias/ajouter/<str:media_type>/', views.ajouter_media, name='ajouter_media'),
    path('medias/<str:media_type>/<int:media_id>/supprimer/', views.supprimer_media, name='supprimer_media'),

    # --- Gestion des emprunts ---
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
    path('emprunts/emprunter/', views.emprunter_media, name='emprunter_media'),
    path('emprunts/<int:emprunt_id>/retourner/', views.retourner_media, name='retourner_media'),

    # --- Pages supplémentaires ---
    path('confirmation-emprunt/', views.confirmation_emprunt, name='confirmation_emprunt'),
    path('limite-emprunts/', views.limite_emprunts, name='limite_emprunts'),
    
]
