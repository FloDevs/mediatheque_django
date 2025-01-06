from django.urls import path
from .views import liste_medias_membre

app_name = 'app_membre'

urlpatterns = [
    path('medias-disponibles/', liste_medias_membre, name='liste_medias_membre'),
]
