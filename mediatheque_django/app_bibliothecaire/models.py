from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Media(models.Model):
    nom = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nom


class Livre(Media):
    auteur = models.CharField(max_length=100)


class DVD(Media):
    realisateur = models.CharField(max_length=100)


class CD(Media):
    artiste = models.CharField(max_length=100)


class JeuDePlateau(Media):
    createur = models.CharField(max_length=100, blank=True, null=True)


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    media = GenericForeignKey('content_type', 'object_id')
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(null=True, blank=True)
    date_prevu_retour = models.DateTimeField(null=True, blank=True)

    @property
    def media_type(self):
        return self.content_type.model

    @property
    def media_id(self):
        return self.object_id

    def valider_emprunt(self):
        if self.membre.bloque:
            raise ValueError("Le membre est bloqué.")
        if not self.media.disponible:
            raise ValueError(f"{self.media} n'est pas disponible.")
        self.media.disponible = False
        self.media.save()
        self.save()

    def retourner_medias(self):
        self.media.disponible = True
        self.media.save()
        self.delete()

    def save(self, *args, **kwargs):
        if not self.pk:  
            emprunts_actifs = Emprunt.objects.filter(membre=self.membre, date_retour__isnull=True).count()
            if emprunts_actifs >= 3:
                raise ValueError("Un membre ne peut pas avoir plus de 3 emprunts actifs.")
            self.date_prevu_retour = self.date_emprunt + timedelta(weeks=1)
        super().save(*args, **kwargs)