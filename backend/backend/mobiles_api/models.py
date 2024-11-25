from django.db import models

from myapi.models import Utilisateur, Cooperative, Certification, Parcelle


# from myapi.models import Cooperative, Utilisateur, Certification, Parcelle
# from ..myapi.models import Cooperative, Utilisateur, Certification, Parcelle


class Technicien(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, null=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.nom + ' ' +self.user.prenom

class Certificat(models.Model):
    code = models.CharField(max_length=255, null=True)
    annee = models.IntegerField(null=True)
    certification = models.ForeignKey(Certification, on_delete=models.SET_NULL, null=True)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.SET_NULL, null=True)