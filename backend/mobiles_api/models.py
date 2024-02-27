from django.db import models

from myapi.models import Cooperative, Utilisateur

class Technicien(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, null=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.nom + ' ' +self.user.prenom
    