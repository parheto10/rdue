from django.db import models

from myapi.models import Campagne, Cooperative, Utilisateur, Certification, Parcelle, Projet

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
    
class CompensationPSE(models.Model):
    code = models.CharField(max_length=255)
    libelle = models.CharField(max_length=255)
    
    def __str__(self):
        return self.libelle
    
class CategorieActiviteRetribution(models.Model):
    libelle = models.CharField(max_length=255)
    
    def __str__(self):
        return self.libelle
    
class ActiviteRetribution(models.Model):
    libelle = models.CharField(max_length=255)
    categorie = models.ForeignKey(CategorieActiviteRetribution, on_delete=models.CASCADE, related_name="activites")
    
    def __str__(self):
        return self.libelle
    
class InfoPSE(models.Model):
    pourcentage_retribution = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    montant_pse = models.IntegerField()
    compensation = models.ForeignKey(CompensationPSE, on_delete = models.SET_NULL, related_name="infos_pse", null = True)
    activites = models.ManyToManyField(ActiviteRetribution)
    projet = models.ForeignKey(Projet, on_delete = models.SET_NULL, related_name="infos_pse", null = True)
    campagne = models.ForeignKey(Campagne, on_delete=models.SET_NULL, related_name="infos_pse", null=True)
    
    def __str__(self):
        return f"{self.projet.nomProjet} {self.campagne.libelle}"