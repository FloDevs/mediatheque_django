from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app_bibliothecaire.models import Membre, Media, Emprunt, Livre, CD, DVD , JeuDePlateau
from django.contrib.contenttypes.models import ContentType

class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        response = self.client.post(reverse('custom_login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('custom_logout'))
        self.assertEqual(response.status_code, 200)





class AuthenticatedTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

class MemberTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.member = Membre.objects.create(nom="John Doe")

    def test_create_member(self):
        response = self.client.post(reverse('ajout_membre'), {'nom': 'Jane Doe'})
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('liste_membres'))  
        self.assertEqual(Membre.objects.count(), 2)  
        self.assertTrue(Membre.objects.filter(nom='Jane Doe').exists())  

    def test_update_member(self):
        response = self.client.post(reverse('mettre_a_jour_membre', args=[self.member.id]), {'nom': 'John Smith'})
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertEqual(self.member.nom, 'John Smith')

    def test_delete_member(self):
        response = self.client.post(reverse('supprimer_membre', args=[self.member.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Membre.objects.count(), 0)

    def test_list_members(self):
        response = self.client.get(reverse('liste_membres'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.member.nom)

class MediaTests(AuthenticatedTestCase):

    def test_ajouter_livre(self):
        response = self.client.post(reverse('ajouter_media', args=['livre']), {
            'nom': 'Livre Exemple',
            'auteur': 'Auteur Exemple'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Livre.objects.count(), 1)
        self.assertEqual(Livre.objects.first().nom, 'Livre Exemple')

    def test_ajouter_dvd(self):
        response = self.client.post(reverse('ajouter_media', args=['dvd']), {
            'nom': 'DVD Exemple',
            'realisateur': 'Réalisateur Exemple'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(DVD.objects.count(), 1)
        self.assertEqual(DVD.objects.first().nom, 'DVD Exemple')

    def test_ajouter_cd(self):
        response = self.client.post(reverse('ajouter_media', args=['cd']), {
            'nom': 'CD Exemple',
            'artiste': 'Artiste Exemple'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(CD.objects.count(), 1)
        self.assertEqual(CD.objects.first().nom, 'CD Exemple')

    def test_ajouter_jeu(self):
        response = self.client.post(reverse('ajouter_media', args=['jeu']), {
            'nom': 'Jeu Exemple',
            'createur': 'Créateur Exemple'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(JeuDePlateau.objects.count(), 1)
        self.assertEqual(JeuDePlateau.objects.first().nom, 'Jeu Exemple')


class EmpruntTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.membre = Membre.objects.create(nom="John Doe", bloque=False)
        self.livre = Livre.objects.create(
            nom="Sample Book", 
            auteur="Author Name", 
            disponible=True
        )
        self.content_type = ContentType.objects.get_for_model(Livre)

    def test_create_emprunt(self):
        response = self.client.post(reverse('emprunter_media'), {
            'membre_id': self.membre.id,
            'media_type': 'livre',
            'media_id': self.livre.id
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Emprunt.objects.count(), 1)
        self.livre.refresh_from_db()
        self.assertFalse(self.livre.disponible)

    def test_emprunt_limit(self):
        livres = [
            Livre.objects.create(
                nom=f"Livre {i}", 
                auteur="Auteur", 
                disponible=True
            ) for i in range(3)
        ]
        
        for livre in livres:
            emprunt = Emprunt.objects.create(
                membre=self.membre,
                content_type=self.content_type,
                object_id=livre.id
            )
            emprunt.valider_emprunt()
        
        response = self.client.post(reverse('emprunter_media'), {
            'membre_id': self.membre.id,
            'media_type': 'livre',
            'media_id': self.livre.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce membre a atteint la limite d&#x27;emprunts")
        self.assertEqual(Emprunt.objects.count(), 3)
