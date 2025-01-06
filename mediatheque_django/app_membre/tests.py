from django.test import TestCase
from django.urls import reverse
from app_bibliothecaire.models import Livre, DVD, CD, JeuDePlateau

class ListeMediasMembreViewTest(TestCase):
    def setUp(self):
        
        self.livre1 = Livre.objects.create(nom="Livre 1", auteur="Auteur1", disponible=True)
        self.livre2 = Livre.objects.create(nom="Livre 2",auteur="Auteur2", disponible=False)
        
        self.dvd1 = DVD.objects.create(nom="DVD 1", realisateur="Real1", disponible=True)
        self.dvd2 = DVD.objects.create(nom="DVD 2", realisateur="Real2", disponible=False)

        self.cd1 = CD.objects.create(nom="CD 1", artiste="artiste1", disponible=True)
        self.cd2 = CD.objects.create(nom="CD 2", artiste="artiste2", disponible=False)

        self.jeu1 = JeuDePlateau.objects.create(nom="Jeu 1", createur="createur1")
        self.jeu2 = JeuDePlateau.objects.create(nom="Jeu 2", createur="createur2")

    def test_liste_medias_membre_view(self):
        response = self.client.get(reverse('app_membre:liste_medias_membre'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.livre1, response.context['livres'])
        self.assertNotIn(self.livre2, response.context['livres'])

        self.assertIn(self.dvd1, response.context['dvds'])
        self.assertNotIn(self.dvd2, response.context['dvds'])

        self.assertIn(self.cd1, response.context['cds'])
        self.assertNotIn(self.cd2, response.context['cds'])

        self.assertIn(self.jeu1, response.context['jeux'])
        self.assertIn(self.jeu2, response.context['jeux'])

        
        self.assertTemplateUsed(response, 'liste_medias_membre.html')



