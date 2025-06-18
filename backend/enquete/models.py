from django.db import models
from mobiles_api.models import Utilisateur, Projet, Campagne

class TypeEnquete(models.Model):
    code = models.CharField(max_length = 15, unique = True)
    libelle = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.libelle}" 

class Enquete(models.Model):
    identifiant = models.CharField(max_length=255, unique=True)
    est_ouverte = models.BooleanField(default = True)
    
    type_enquete = models.ForeignKey(TypeEnquete, on_delete = models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete = models.CASCADE)
    campagne = models.ForeignKey(Campagne, on_delete = models.CASCADE)
    created_by = models.ForeignKey(Utilisateur, on_delete = models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.identifiant

class TypeQuestion(models.Model):
    libelle = models.CharField(max_length=255, unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.libelle

class Question(models.Model):
    libelle = models.CharField(max_length=255)
    est_obligatoire = models.BooleanField(default=True)
    choix = models.JSONField(blank=True, null = True)
    type_question = models.ForeignKey(TypeQuestion, on_delete = models.CASCADE)
    enquete = models.ForeignKey(Enquete, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.libelle
    
class Condition(models.Model):
    question_principale = models.ForeignKey(Question, on_delete = models.CASCADE)
    valeur = models.CharField(max_length=255)
    question_cible = models.ForeignKey(Question, on_delete = models.CASCADE, related_name='conditions')
    
    def __str__(self):
        return f"{self.question_principale} - {self.valeur} - {self.question_cible}"
    
class Reponse(models.Model):
    enquete  = models.ForeignKey(Enquete, on_delete = models.CASCADE)
    repondant = models.ForeignKey(Utilisateur, on_delete = models.CASCADE)
    reponses = models.JSONField()
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.enquete.identifiant} - {self.repondant.nom}  {self.repondant.prenom}"

class Enqueteur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, null=True)
    enquetes = models.ManyToManyField(Enquete)
    
    def __str__(self):
        return self.user.nom + ' ' + self.user.prenom