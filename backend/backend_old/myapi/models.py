# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from django.core import serializers
from django.db import models
from django.db.models import Sum
from PIL import Image
from django_resized import ResizedImageField
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q

# Create your models here.

def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.nomProjet + ".jpeg"

GENRE = (
    ('HOMME', "HOMME"),
    ('FEMME', "FEMME"),
)

CHOIX = (
    ('OUI', 'OUI'),
    ('NON', 'NON'),
)

TYPE_MAIN_DOEUVRE = (
    ('FAMILLE', 'FAMILLE'),
    ('EXTERIEURE', 'EXTERIEURE'),
)

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'Adresse e-mail est requise')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_online', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class Countrie(models.Model):
    libelle = models.CharField(max_length=200) 
    code = models.CharField(max_length=50)
     
    class Meta:
        verbose_name_plural = "01. Pays"
        
    def __str__(self):
        return '%s' %(self.libelle) 
    

class Utilisateur(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True,null=True,blank=True)
    nom = models.CharField(max_length=100,null=True)
    prenom = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100,null=True,blank=True,unique=True)
    tel = models.CharField(max_length=100,null=True)
    sexe = models.CharField(max_length=50,null=True)
    date_adh_agromap = models.DateField(null=True,blank=True)
    fonction = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=300)
    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    #role users
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_responsable = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_gestionnaire = models.BooleanField(default=False)
    is_adg = models.BooleanField(default=False)
    is_technicien = models.BooleanField(default=False)
    is_pepinieriste = models.BooleanField(default=False)
    
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        null=True,
        help_text=('Specific permissions for the user utilisateur.'),
        related_name='utilisateurs'  # Utilisation d'un nom de requête inverse personnalisé
    )
    permission_ptr = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        parent_link=True,
        null=True,
        blank=True,
        related_name='utilisateur'  # Utilisation d'un nom de requête inverse personnalisé
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name_plural = "02. Utilisateurs"
        
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
        
class Projet(models.Model):
    nomProjet = models.CharField(max_length=100,null=True)
    countrie = models.ForeignKey(Countrie,on_delete=models.CASCADE,null=True)
    description = models.TextField(null=True,blank=True)
    dateDebut = models.DateField(null=True,blank=True)
    dateFin = models.DateField(null=True,blank=True)
    objectif = models.CharField(max_length=100,null=True,blank=True) #defini quel type de projet il s'agit agroforesterie,reforestation,mangrove
    etat = models.BooleanField(default=True)
    plant_aproduit = models.FloatField(default=0)
    carbon_astock = models.FloatField(default=0)
    emp_engageof_proj = models.IntegerField(default=0)
    logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
    #new
    respo = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' %(self.nomProjet) 
    
    
    class Meta:
        verbose_name_plural = "03. Projets"

    def total_coop_projet(self):
        total_coop_projet = Cooperative.objects.filter(projet=self).count()
        return total_coop_projet

    def total_producteurs_projet(self):
        total_producteurs_projet = Producteur.objects.filter(section__cooperative__projet=self).count()
        return total_producteurs_projet

    def total_parcelles_projet(self):
        total_parcelles_projet = Parcelle.objects.filter(producteur__section__cooperative__projet=self).count()
        return total_parcelles_projet
    
    def total_superficie_projet(self):
        total_superficie_projet = Parcelle.objects.filter(producteur__section__cooperative__projet=self).aggregate(total=Sum('superficie'))['total']
        return total_superficie_projet
    
    def total_arbres_projet(self):
        total_superficie_projet = DetailPlanting.objects.filter(planting__parcelle__producteur__section__cooperative__projet=self).aggregate(total=Sum('plants'))['total']
        return total_superficie_projet

    def total_parcelles_proj_risk_modere(self):
        total_parcelles_proj_risk_modere = Parcelle.objects.filter(risque=2).filter(producteur__section__cooperative__projet=self).count()
        # total_parcelles_coop_risk_modere = Parcelle.objects.filter(risque__parcelle=2).filter(producteur__section__cooperative=self).count()
        print(total_parcelles_proj_risk_modere)
        return total_parcelles_proj_risk_modere

    def total_parcelles_proj_risk_zero(self):
        total_parcelles_proj_risk_zero = Parcelle.objects.filter(producteur__section__cooperative__projet=self).filter(risque=3).count()
        print(total_parcelles_proj_risk_zero)
        return total_parcelles_proj_risk_zero
        
class UserProjet(models.Model):
    utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,null=True)
    projet = models.ForeignKey(Projet,on_delete=models.CASCADE,null=True)
    etatuser = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "04. Users on projects"
        
        
class Campagne(models.Model):
    libelle = models.CharField(max_length=200,null=True,blank=True)
    dateDebut = models.DateField(null=True,blank=True)
    DateFin = models.DateField(null=True,blank=True)
    etat =  models.BooleanField(default=True)
    duree_campagne = models.CharField(max_length=100,null=True,blank=True)
    respo = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,null=True)#le createur d'une campagne
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s - %s' %(self.libelle, self.respo.email)
    
    
    class Meta:
        verbose_name_plural = "05. Campagnes"
        ordering = ["-created_at"]

class CategorieEspece(models.Model):
    libelle = models.CharField(max_length=100,unique=True)
    
    class Meta:
        verbose_name_plural = "06. Categories especes"  
        
    def __str__(self):
        return '%s' %(self.libelle) 

class Espece(models.Model):
    categorie = models.ForeignKey(CategorieEspece,on_delete=models.CASCADE,null=True)
    accronyme = models.CharField(max_length=250, verbose_name="NOM SCIENTIFIQUE")
    libelle = models.CharField(max_length=250, verbose_name="NOM USUEL",unique=True)
    densite = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="DENSITE SPECIFIQUE", default=0)
    hmax = models.FloatField(default=0)
    dmax = models.FloatField(default=0)
    co2_annuel = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="CO2/AN", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "07. Especes"
        ordering = ["libelle"]
        
    def __str__(self):
        return '%s' %(self.libelle) 
    

class SimulateCarbon(models.Model):
    anneePeuplement = models.IntegerField(default=1)
    code = models.CharField(max_length=100,null=True,blank=True)
    totalCarbone = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "08. Simulation carbone"
    
    def __str__(self):
        return '%s' %(self.code) 
    
class EspeceSimulate(models.Model):
    simulate = models.ForeignKey(SimulateCarbon,on_delete=models.CASCADE,null=True)
    espece = models.ForeignKey(Espece,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    carboneStocke = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "09. Especes de simulation"
        
    def __str__(self):
        return '%s' %(self.simulate) 
    

class CampagneProjet(models.Model):
    campagne = models.ForeignKey(Campagne,on_delete=models.CASCADE,null=True)
    projet = models.ForeignKey(Projet,on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name_plural = "10. Campagnes par projets"
    def __str__(self):
        return '%s' %(self.projet) 

class Region(models.Model):
    libelle = models.CharField(max_length=250,null=True,blank=True)
    countrie = models.ForeignKey(Countrie,on_delete=models.CASCADE,null=True)
    chef_lieu_reg = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "11. Regions"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 

class Cooperative(models.Model):
    region = models.ForeignKey(Region,on_delete=models.CASCADE,null=True)
    respCoop = models.CharField(max_length=255, blank=True, null=True)
    numConnaissement = models.CharField(max_length=255, blank=True, null=True)
    numRegistre = models.CharField(max_length=255, blank=True, null=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True, blank=True)
    nomCoop = models.CharField(max_length=500,blank=True, null=True)
    contacts = models.CharField(max_length=50,blank=True, null=True)
    logo = models.ImageField(upload_to='logo_coop/',null=True)
    etat = models.BooleanField(default=True)
    siege = models.CharField(max_length=50,blank=True, null=True)
    respo = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,null=True)#l'unique createur de cooperative
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "12. Cooperatives"
    
    def __str__(self):
        return '%s' %(self.nomCoop) 
    
    def total_producteurs_coop(self):
        total_producteurs_coop = Producteur.objects.filter(section__cooperative=self).count()
        return total_producteurs_coop

    
    def total_sections_coop(self):
        total_sections_coop = Section.objects.filter(cooperative=self).count()
        return total_sections_coop

    def total_production_coop(self):
        total_sections_coop = RecolteProducteur.objects.filter(parcelle__producteur__section__cooperative=self).aggregate(total=Sum('poids_total'))['total']
        print(total_sections_coop)
        return total_sections_coop
    
    def total_parcelles_coop(self):
        total_parcelles_coop = Parcelle.objects.filter(producteur__section__cooperative=self).count()
        return total_parcelles_coop

    def total_parcelles_sup_4ha(self):
        total_parcelles_sup_4ha = Parcelle.objects.filter(producteur__section__cooperative=self).filter(superficie__gt=4.00).count()
        nb_total_parcelles_sup_4ha = len(Parcelle.objects.filter())
        print(nb_total_parcelles_sup_4ha)
        return total_parcelles_sup_4ha

    def pourcentage_parcelles_sup_4ha(self):
        pourcentage_parcelles_sup_4ha = (float(self.total_parcelles_sup_4ha()) / float(self.total_parcelles_coop())) * 100
        print(pourcentage_parcelles_sup_4ha)
        return pourcentage_parcelles_sup_4ha

    def total_parcelles_inf_4ha(self):
        total_parcelles_sup_4ha = Parcelle.objects.filter(producteur__section__cooperative=self).filter(superficie__lte=4.00).count()
        return total_parcelles_sup_4ha

    def pourcentage_parcelles_inf_4ha(self):
        pourcentage_parcelles_inf_4ha = (self.total_parcelles_inf_4ha / self.total_parcelles_coop) * 100
        print(pourcentage_parcelles_inf_4ha)
        return pourcentage_parcelles_inf_4ha

    def total_parcelles_coop_risk_eleve(self):
        total_parcelles_coop_risk_eleve = Parcelle.objects.filter(producteur__section__cooperative=self).filter(risque=1).count()
        return total_parcelles_coop_risk_eleve

    def total_parcelles_coop_risk_modere(self):
        total_parcelles_coop_risk_modere = Parcelle.objects.filter(risque=2).filter(producteur__section__cooperative=self).count()
        # total_parcelles_coop_risk_modere = Parcelle.objects.filter(risque__parcelle=2).filter(producteur__section__cooperative=self).count()
        print(total_parcelles_coop_risk_modere)
        return total_parcelles_coop_risk_modere

    def total_parcelles_coop_risk_zero(self):
        total_parcelles_coop_risk_zero = Parcelle.objects.filter(producteur__section__cooperative=self).filter(risque=3).count()
        #print(total_parcelles_coop_risk_zero)
        return total_parcelles_coop_risk_zero
    
    def total_parcelles_a_risque(self):
        total_parcelles_a_risque = Parcelle.objects.filter(producteur__section__cooperative=self).filter(Q(risque=2) | Q(risque=1)).count()
        #print(total_parcelles_a_risque)
        return total_parcelles_a_risque

    def sumSuperficieRisqueModere(self):
        sumSuperficieRisqueModere = Parcelle.objects.filter(producteur__section__cooperative=self).filter(risque_id=2).aggregate(total=Sum('superficie'))
        return sumSuperficieRisqueModere
    
    def sumSuperficie(self):
        sumSuperficie = Parcelle.objects.filter(producteur__section__cooperative=self).aggregate(total=Sum('superficie'))
        return sumSuperficie

    def sumSuperficieInf4ha(self):
        sumSuperficieInf4ha = Parcelle.objects.filter(producteur__section__cooperative=self).filter(superficie__lte=4).aggregate(total=Sum('superficie'))
        return sumSuperficieInf4ha

    def sumSuperficieSup4ha(self):
        sumSuperficieSup4ha = Parcelle.objects.filter(producteur__section__cooperative=self).filter(superficie__gt=4).aggregate(total=Sum('superficie'))
        return sumSuperficieSup4ha
    
    def sumPlantCoop(self):
        sumPlantCoop = DetailPlanting.objects.filter(planting__parcelle__producteur__section__cooperative=self).aggregate(total=Sum('plants'))
        return sumPlantCoop
    
    def carbonStockeCoop(self):
        quantity = 0
        especePlantes = DetailPlanting.objects.filter(planting__parcelle__producteur__section__cooperative=self)
        for espece in especePlantes :
            quantity = (espece.plants * float(espece.espece.co2_annuel)* 1) * 0.001
            
        return quantity
        
        
    

class Section(models.Model):
    cooperative = models.ForeignKey(Cooperative,on_delete=models.CASCADE, null=True)
    libelle = models.CharField(max_length=250,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "13. Sections"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 
    
class GroupeProducteur(models.Model):
    libelle = models.CharField(max_length=250,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "14. Groupe de producteurs"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 
    
class Producteur(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    # genre = models.CharField(max_length=2, choices=GENRE, default="H")
    nomComplet = models.CharField(max_length=250,blank=True, null=True)
    contacts = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='photo_prod/',null=True)
    nbParc = models.IntegerField(default=0)
    etat = models.BooleanField(default=True)#actif ou pas
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, null=True)
    lieu_habitation = models.CharField(max_length=150,blank=True, null=True)
    #communaute
    groupe = models.ForeignKey(GroupeProducteur, on_delete=models.CASCADE, null=True)
    representant = models.CharField(max_length=250,blank=True, null=True)
    nbreMembre = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "15. Producteurs"
    
    def __str__(self):
        return '%s-%s' %(self.code,self.nomComplet) 
    
    def total_parcelle_prod(self):
        total_parcelle_prod = Parcelle.objects.filter(producteur=self).count()
        return total_parcelle_prod

class Culture(models.Model):
    libelle = models.CharField(max_length=250,blank=True, null=True)
    cooperative = models.ForeignKey(Cooperative,on_delete=models.CASCADE,null=True)
    prix_unitaire_culture = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "16. Cultures"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 

class ModeAcquisition(models.Model):
    libelle = models.CharField(max_length=250,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "17. Mode d'acquisition"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 
    
class Certification(models.Model):
    libelle = models.CharField(max_length=250,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "27. CERTIFICATION PARCELLE"
        ordering = ["libelle"] 
    
    def __str__(self):
        return '%s' %(self.libelle)


class Acte_Propriete(models.Model):
    libelle = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "41. ACTE DE PROPRIETE"
        ordering = ["libelle"]

    def save(self, force_insert=False, force_update=False, using=None):
        self.libelle = self.libelle.upper()
        super(Acte_Propriete, self).save(force_insert, force_update, using)

    def __str__(self):
        return '%s' % (self.libelle)


class RisqueRDUE(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, null=True)
    libelle = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "28. RISQUES RDUE"
        ordering = ["libelle"]

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False, using=None):
        self.libelle = self.libelle.upper()
        super(RisqueRDUE, self).save(force_insert, force_update, using)
     

class Parcelle(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
    risque = models.ForeignKey(RisqueRDUE, on_delete=models.CASCADE,null=True)
    producteur = models.ForeignKey(Producteur, on_delete=models.CASCADE,null=True)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, null=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    #contour = models.TextField(null=True,blank=True)
    superficie = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # superficie = models.FloatField(default=0)
    is_doc_propriete = models.BooleanField(default=False)
    certificat = models.ForeignKey(Certification, on_delete=models.CASCADE, null=True)
    type_acte_propriete = models.ForeignKey(Acte_Propriete, on_delete=models.CASCADE, null=True)
    doc_acte_propriete = models.FileField(upload_to='Documents/%Y/%m/%d', null=True, blank=True)
    code_certif = models.CharField(max_length=150, null=True, blank=True)
    annee_certificat = models.CharField(max_length=150, null=True, blank=True)
    annee_acquis = models.CharField(max_length=150, null=True, blank=True)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, null=True)
    acquisition = models.ForeignKey(ModeAcquisition, on_delete=models.CASCADE, null=True)
    is_mapped = models.BooleanField(default=False)
    fichier_de_mappage = models.FileField(upload_to='fichier_mapping/', null=True, blank=True)


    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "18. Parcelles"
    
    def __str__(self):
        return '%s-%s' %(self.code,self.producteur.nomComplet) 

class Planting(models.Model):
    code = models.CharField(max_length=150, unique=True, primary_key=True)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, null=True)
    plant_existant = models.IntegerField(default=0)
    plant_recus = models.IntegerField(default=0)
    note_plant_existant = models.TextField(null=True)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "19. Plantings"
        ordering = ["-created_at"]
        
    def __str__(self):
        return '%s-%s-%s' %(self.code,self.parcelle.code,self.parcelle.producteur.nomComplet) 
    
    def total_monitoring(self):
        total_monitoring = Monitoring.objects.filter(planting=self).count()
        return total_monitoring
    
    def total_espece_plante(self):
        total_espece_plante = DetailPlanting.objects.filter(planting=self).count()
        return total_espece_plante
    
    def detail_planting_see(self):
        plants = DetailPlanting.objects.filter(planting=self)
        return serializers.serialize('json',plants)
    

class DetailPlanting(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE,null=True)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, null=True)
    plants = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "20. Especes Plantées"
        ordering = ["-created_at"]

    def __str__(self):
        return '%s-%s' %(self.code,self.planting.parcelle.code) 
    

class Monitoring(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE,null=True)
    #plant_denombre_total = models.IntegerField(default=0)
    date = models.DateField(null=True,blank=True)
    taux_reussite = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "21. Monitoring"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.code}"
    
    def sumPlantEspece(self):
        sumPlantEspece = MonitoringDetail.objects.filter(monitoring=self).aggregate(total=Sum('plant_denombre'))
        return sumPlantEspece
    
class MonitoringDetail(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
    monitoring = models.ForeignKey(Monitoring,on_delete=models.CASCADE,null=True)
    espece = models.ForeignKey(Espece,on_delete=models.CASCADE,null=True)
    plant_denombre = models.IntegerField(default=0)
    taux_reussite = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name_plural = "22. Monitoring par espèces"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.code}"
    

class ObservationMortalite(models.Model):
    libelle = models.CharField(max_length=200,null=True,blank=True)
     
    class Meta:
        verbose_name_plural = "23. Cause de mortalite"
        ordering = ["libelle"]
        
    def __str__(self):
        return '%s' %(self.libelle) 
    
class ObservationMonitoring(models.Model):
    monitoring = models.ForeignKey(Monitoring,on_delete=models.CASCADE,null=True)
    observation = models.ForeignKey(ObservationMortalite,on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name_plural = "24. Observations monitoring"
        
    def __str__(self):
        return f"{self.monitoring.code}=>{self.observation.libelle}"
    

class SaisonRecolte(models.Model):
    libelle = models.CharField(max_length=250,null=True,blank=True)
    cooperative = models.ForeignKey(Cooperative,on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name_plural = "25. Saisons de recolte"
        
    def __str__(self):
        return f"{self.libelle}" 
    
class RecolteProducteur(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
    parcelle = models.ForeignKey(Parcelle,on_delete=models.CASCADE,null=True)
    campagne = models.ForeignKey(Campagne,on_delete=models.CASCADE,null=True)
    saison = models.ForeignKey(SaisonRecolte,on_delete=models.CASCADE,null=True)
    culture = models.ForeignKey(Culture,on_delete=models.CASCADE,null=True)
    estimation_production = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    nbre_sacs = models.IntegerField(default=0)
    poids_total = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    prix_total = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "26. Recoltes producteurs"
        
    def __str__(self):
        return f"{self.code}-{self.parcelle.producteur.nomComplet}"



####################################################### ANALYSE RDUE ###################################################
CHOIX = (
    ("OUI", "OUI"),
    ("NON", "NON"),
)

ACTIVITE_CONTROVERSE = (
    ("EXPLOITATION ILLEGALE DU BOIS", "EXPLOITATION ILLEGALE DU BOIS"),
    ("ORPAILLAGE", "ORPAILLAGE"),
    ("DEFORESTATION", "DEFORESTATION"),
    ("TRAVAIL DES ENFANTS", "TRAVAIL DES ENFANTS"),
    ("AUCUN", "AUCUN"),
)

COOP_CHOICE = (
    ('AGRIAL', 'AGRIAL'),
    ('COOPAA-HS', 'COOPAA-HS'),
)


CHAINE_APPRO_CHOICES = (
    ('MEMBRES', 'MEMBRES'),
    ('AUTRE', 'AUTRE')
)

PRODUIDE_CHOICES = (
    ('CACAO', 'CACAO'),
    ('CAFE', 'CAFE'),
    ('HEVEAS', 'HEVEAS'),
    ('SOJA', 'SOJA'),
    ('PALMIER', 'PALMIER A HUILE'),
    ('BOIS', 'BOIS'),
    ('BOEUF', 'BOEUF'),
    # ('AUTRE', 'AUTRE'),
)
class RDUE(models.Model):
    evaluateur = models.CharField(max_length=255, null=True, blank=True, verbose_name="ENQUETEUR")
    entite = models.ForeignKey(Cooperative, on_delete=models.CASCADE, verbose_name="ORGANISATION")
    produits = models.CharField(max_length=255,choices=PRODUIDE_CHOICES, verbose_name="PRODUITS COMMERCIALISES", default="CACAO")
    chaine_appro = models.CharField(max_length=255, null=True, blank=True,choices=CHAINE_APPRO_CHOICES,  verbose_name="APPROVISIONNEMENT", default="MEMBRES")
    pays_origine = models.ForeignKey(Countrie, on_delete=models.CASCADE, verbose_name="PAYS D'ORIGINE", default=1)
    zone_arisque = models.CharField(choices=ACTIVITE_CONTROVERSE, max_length=255, default="AUCUN", verbose_name="Activités portant à controverse")
    mesure_preventives = models.TextField(blank=True, null=True, verbose_name="Mesures Correctives")
    suivi_mesure = models.TextField(blank=True, null=True)
    efficacite_mesure = models.TextField(blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "29. QUESTIONNAIRES RDUE"
        # ordering = ["libelle"]


################################################# ENQUETES #############################################################
class Age(models.Model):
    libelle = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name_plural = "30. TRANCHES AGES"
        # ordering = ["libelle"]

class Theme_Enquete(models.Model):
    libelle = models.CharField(max_length=255)

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name_plural = "31. THEMATIQUES ENQUETES"
        ordering = ["libelle"]

class Produit_Phyto(models.Model):
    libelle = models.CharField(max_length=255)

    def __str__(self):
        return self.libelle
    class Meta:
        verbose_name_plural = "32. PRODUITS PHYTO"
        ordering = ["libelle"]

class Engrais(models.Model):
    libelle = models.CharField(max_length=255)

    def __str__(self):
        return self.libelle
    class Meta:
        verbose_name_plural = "33. ENGRAIS"
        ordering = ["libelle"]

    def save(self, force_insert=False, force_update=False, using=None):
        self.libelle = self.libelle.upper()
        super(Engrais, self).save(force_insert, force_update, using)

class Enquete_Social(models.Model):
    thematique = models.ForeignKey(Theme_Enquete, on_delete=models.CASCADE, verbose_name="THEMATIQUE", related_name="enquetes_thematiques")
    producteur = models.ForeignKey(Producteur, related_name="enquetes_producteur", on_delete=models.CASCADE)
    nb_epouse = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NBRE D'EPOUSE ")
    nb_enfant = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NBRE TOTAL D'ENFANTS")
    nb_personne = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="PERSONNES A CHARGE")
    is_compte_bancaire = models.BooleanField(default=False)
    is_mobile_money = models.BooleanField(default=False)
    numero_mobile_money = models.CharField(max_length=10, null=True, blank=True)
    revenu_moyen = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "34. ENQUETES SOCIALES"
        ordering = ["thematique"]

    # def save(self, force_insert=False, force_update=False, using=None):
    #     self.libelle = self.libelle.upper()
    #     super(Enquete_Social, self).save(force_insert, force_update, using)


class Age_enfant(models.Model):
    enquete_social = models.ForeignKey(Enquete_Social, on_delete=models.CASCADE, related_name="age_enfant_enquetes")
    age = models.ForeignKey(Age, on_delete=models.CASCADE, related_name="age_enfant", verbose_name="AGE")
    nombre_enfant = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NOMBRE ENFANT")

    class Meta:
        verbose_name_plural = "35. AGE ENFANTS"
        # ordering = ["thematique"]

class Age_scolarise(models.Model):
    enquete_social = models.ForeignKey(Enquete_Social, on_delete=models.CASCADE, related_name="age_enfant_scolarise")
    age = models.ForeignKey(Age, on_delete=models.CASCADE, related_name="age_enfant_scolarise", verbose_name="AGE")
    nombre_enfant_scolarise = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NOMBRE ENFANT SCOLARISE")

    class Meta:
        verbose_name_plural = "36. AGE ENFANTS SCOLARISES"
        # ordering = ["thematique"]


class Enquete_Exploitation(models.Model):
    thematique = models.ForeignKey(Theme_Enquete, on_delete=models.CASCADE, verbose_name="THEMATIQUE")
    Parcelle = models.ForeignKey(Parcelle, related_name="enquete_parcelle", on_delete=models.CASCADE)
    culture_principale = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name="enquete_culture_principale")
    culture_secondaire= models.ForeignKey(Culture, on_delete=models.CASCADE, related_name="enquete_culture_secondaire", null=True, blank=True)

    is_main_doeuvre_homme = models.BooleanField(default=False)
    nb_main_doeuvre_homme = models.PositiveIntegerField(default=0, null=True, blank=True)
    salaire_moyen_homme = models.PositiveIntegerField(default=0, null=True, blank=True)

    is_main_doeuvre_femme = models.BooleanField(default=False)
    nb_main_doeuvre_femme = models.PositiveIntegerField(default=0, null=True, blank=True)
    salaire_moyen_femme = models.PositiveIntegerField(default=0, null=True, blank=True)

    is_produit_phyto = models.BooleanField(default=False)
    is_engrais = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "37. ENQUETES EXPLOITATION"
        # ordering = ["thematique"]


class Detail_Age_Homme(models.Model):
    enquete_exploitation = models.ForeignKey(Enquete_Exploitation, on_delete=models.CASCADE)
    age_homme = models.ForeignKey(Age, on_delete=models.CASCADE)
    nombre_homme = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "38. DETAILS AGE MAIN D'OEUVRE HOMMES"
        # ordering = ["thematique"]


class Detail_Age_Femme(models.Model):
    enquete_exploitation = models.ForeignKey(Enquete_Exploitation, on_delete=models.CASCADE)
    age_femme = models.ForeignKey(Age, on_delete=models.CASCADE)
    nombre_femme = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "39. DETAILS AGE MAIN D'OEUVRE FEMME"
        # ordering = ["thematique"]


class Detail_phyto(models.Model):
    enquete_exploitation = models.ForeignKey(Enquete_Exploitation, on_delete=models.CASCADE)
    produits_phyto = models.ForeignKey(Produit_Phyto, on_delete=models.CASCADE)
    nom_produit = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "39. DETAILS PRODUITS PHYTO"
        # ordering = ["thematique"]


class Detail_Engrais(models.Model):
    enquete_exploitation = models.ForeignKey(Enquete_Exploitation, on_delete=models.CASCADE)
    engrais = models.ForeignKey(Engrais, on_delete=models.CASCADE)
    nom_engrais = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name_plural = "40. DETAILS ENGRAIS"
        # ordering = ["thematique"]

class SectionPoint(models.Model):
    cooperative = models.ForeignKey(Cooperative,on_delete=models.CASCADE, null=True)
    libelle = models.CharField(max_length=250,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "41. Sections Points"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 
    



POINT_TYPE = (
    ('ECOLE', "ECOLE"),
    ('HOPITAL', "HOPITAL"),
)
    
class Point(models.Model):
    section = models.ForeignKey(SectionPoint, on_delete=models.CASCADE, null=True)
    point_type = models.CharField(max_length=20, choices=POINT_TYPE, blank=True, null=True)
    libelle = models.CharField(max_length=250,blank=True, null=True)
    contacts = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='photo_point/',null=True, blank=True)

    class Meta:
        verbose_name_plural = "42. Points"
        ordering = ["libelle"]
    
    def __str__(self):
        return '%s' %(self.libelle) 

# class Enquete(models.Model):
#     producteur = models.ForeignKey(Producteur, related_name="enquetes_producteur", on_delete=models.CASCADE)
#     nb_epouse = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NBRE D'EPOUSE ")
#     enfant_mineur = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="ENFANTS MINEURS")
#     enfant_majeur = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="ENFANTS MAJEURS")
#     nb_enfant = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NBRE TOTAL D'ENFANTS")
#     enfant_scolarise = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="ENFANTS SCOLARISES")
#     nb_personne = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="PERSONNES A CHARGE")
#     is_manoeuvre = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="UTILISEZ-VOUS DES MANOEUVRES ?")
#     is_manoeuvre_femme = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="Recours aux femmes comme main d'œuvre dans l'activité")
#     nb_manoeuvre_femme = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NB FEMME MANOEUVRE")
#     type_manoeuvre = models.CharField(max_length=10, choices=TYPE_MAIN_DOEUVRE, blank=True, null=True)
#     nb_manoeuvre = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NBRE DE MANOEUVRES")
#     is_ouvrier_mineur = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="UTILISEZ-VOUS DES MANOEUVRES MINEURS")
#     nb_ouvrier_mineur = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NBRE DE MANOEUVRES MINEURS")
#     salaire_ouvrier = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="SALAIRE MOYEN/OUVRIER")
#
#     utilisation_produit_phyto = models.CharField(max_length=10, choices=CHOIX)
#
#
#     is_eau_potable = models.BooleanField(default=False, verbose_name="ACCES EAU POTABLE")
#     is_electricite = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="ACCES ELECTRICITE")
#     is_soins = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="ACCES AUX SOINS")
#     nb_dispensaire = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NOMBRE DE CENTRE DE SANTE DANS LA LOCALITE")
#     dtce_dispensaire = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="DISTANCE MOYENNE AU CENTRE DE SANTE LE PLUS PROCHE")
#     nb_ecole_primaire = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NOMBRE D'ECOLES PRIMARE DANS LA LOCALITE")
#     dtce_ecole_primaire = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="DISTANCE MOYENNE A L'ECOLE PRIMAIRE LA PLUS PROCHE")
#     is_college = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="LA LOCALITE DISPOSE-T-ELLE D'UN COLLEGE/LYCEE ?")
#     nb_college = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NOMBRE DE COLLEGES/LYCEE DANS LA LOCALITE")
#     dtce_college = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="DISTANCE MOYENNE COLLEGE/LYCEE LE PLUS PROCHE")
#     is_banque = models.CharField(max_length=10, choices=CHOIX, blank=True, null=True, verbose_name="LA LOCALITE DISPOSE-T-ELLE D'ETABLISSEMENT FINACIER ?")
#     nb_banque = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="NOMBRE D'ETABLISSEMENT FINACIER DANS LA LOCALITE")
#     dtce_banque = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="DISTANCE MOYENNE ETABLISSEMENT FINACIER LE PLUS PROCHE")
#
#     # evaluateur = models.CharField(max_length=255, null=True, blank=True, verbose_name="NOM ET PRENOMS")
#     # producteur = models.ForeignKey(Producteur, on_delete=models.CASCADE, related_name="producteur_enqueter")
#     # add_le = models.DateTimeField(auto_now_add=True)
#     # update_le = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural = "31. ENQUETES SOCIALE"
#         # ordering = ["libelle"]
