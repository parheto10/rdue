import datetime
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,Permission
from django.core import serializers
from django.db import models
from django.db.models import Sum
from PIL import Image
from django_resized import ResizedImageField
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.

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
    #new
    respo = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' %(self.nomProjet) 
    
    
    class Meta:
        verbose_name_plural = "03. Projets"
        
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
        return '%s' %(self.libelle) 
    
    
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
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True)
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
    
    def total_parcelles_coop(self):
        total_parcelles_coop = Parcelle.objects.filter(producteur__section__cooperative=self).count()
        return total_parcelles_coop

    def total_parcelles_sup_4ha(self):
        total_parcelles_sup_4ha = Parcelle.objects.filter(producteur__section__cooperative=self).filter(superficie__gte=4).count()
        nb_total_parcelles_sup_4ha = len(Parcelle.objects.filter())
        print(nb_total_parcelles_sup_4ha)
        return total_parcelles_sup_4ha

    def pourcentage_parcelles_sup_4ha(self):
        pourcentage_parcelles_sup_4ha = (float(self.total_parcelles_sup_4ha()) / float(self.total_parcelles_coop())) * 100
        print(pourcentage_parcelles_sup_4ha)
        return pourcentage_parcelles_sup_4ha

    def total_parcelles_inf_4ha(self):
        total_parcelles_sup_4ha = Parcelle.objects.filter(producteur__section__cooperative=self).filter(superficie__lt=4).count()
        return total_parcelles_sup_4ha

    def pourcentage_parcelles_inf_4ha(self):
        pourcentage_parcelles_inf_4ha = (self.total_parcelles_inf_4ha / self.total_parcelles_coop) * 100
        print(pourcentage_parcelles_inf_4ha)
        return pourcentage_parcelles_inf_4ha

    def total_parcelles_coop_risk_eleve(self):
        total_parcelles_coop_risk_eleve = Parcelle.objects.filter(producteur__section__cooperative=self).filter(risque=1).count()
        return total_parcelles_coop_risk_eleve

    def total_parcelles_coop_risk_modere(self):
        total_parcelles_coop_risk_modere = Parcelle.objects.filter(risque="2").filter(producteur__section__cooperative=self).count()
        # total_parcelles_coop_risk_modere = Parcelle.objects.filter(risque__parcelle=2).filter(producteur__section__cooperative=self).count()
        print(total_parcelles_coop_risk_modere)
        return total_parcelles_coop_risk_modere

    def total_parcelles_coop_risk_zero(self):
        total_parcelles_coop_risk_zero = Parcelle.objects.filter(producteur__section__cooperative=self).filter(risque=3).count()
        print(total_parcelles_coop_risk_zero)
        return total_parcelles_coop_risk_zero
    
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
    is_mapped = models.BooleanField(default=False)
    superficie = models.FloatField(default=0)
    
    # certificat = models.ForeignKey(Certification, on_delete=models.CASCADE, null=True)
    # code_certif = models.CharField(max_length=150, null=True, blank=True)
    # annee_certificat = models.CharField(max_length=150, null=True, blank=True)
    annee_acquis = models.CharField(max_length=150, null=True, blank=True)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, null=True)
    acquisition = models.ForeignKey(ModeAcquisition, on_delete=models.CASCADE, null=True)
    titre_de_propriete = models.CharField(max_length=255, null=True)
    image_du_titre_de_propriete = models.ImageField(upload_to='titre_de_propriete/', null=True)
    fichier_de_mappage = models.ImageField(upload_to='fichier_mapping/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "18. Parcelles"
    
    def __str__(self):
        return '%s-%s' %(self.code,self.producteur.nomComplet) 
    
    
class Planting(models.Model):
    code = models.CharField(max_length=150,unique=True,primary_key=True)
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
    producteur = models.ForeignKey(Producteur,on_delete=models.CASCADE,null=True)
    campagne = models.ForeignKey(Campagne,on_delete=models.CASCADE,null=True)
    saison = models.ForeignKey(SaisonRecolte,on_delete=models.CASCADE,null=True)
    culture = models.ForeignKey(Culture,on_delete=models.CASCADE,null=True)
    lieu_production = models.CharField(max_length=200,blank=True,null=True)
    nbre_sacs = models.IntegerField(default=0)
    poids_total = models.FloatField(default=0)
    prix_total = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "26. Recoltes producteurs"
        
    def __str__(self):
        return f"{self.code}-{self.producteur.nomComplet}"



#### ANALYSE RDUE ################################################################
CHOIX = (
    ("OUI", "OUI"),
    ("NON", "NON"),
)

COOP_CHOICE = (
    ('AGRIAL', 'AGRIAL'),
    ('COOPAA-HS', 'COOPAA-HS'),
)

class RDUE(models.Model):
    evaluateur = models.CharField(max_length=255, null=True, blank=True)
    entite = models.CharField(max_length=255, choices=COOP_CHOICE)
    produits = models.CharField(max_length=255, blank=True, null=True)
    chaine_appro = models.TextField(blank=True, null=True)
    pays_origine = models.CharField(max_length=150, blank=True, null=True)
    # fournisseur = models.CharField(max_length=150, blank=True, null=True)
    zone_arisque = models.CharField(choices=CHOIX, max_length=10, default="NON")
    liste_zone = models.CharField(max_length=250, blank=True, null=True)
    exp_illegale = models.CharField(choices=CHOIX, max_length=10, default="NON")
    mesure_preventives = models.TextField(blank=True, null=True)
    suivi_mesure = models.TextField(blank=True, null=True)
    efficacite_mesure = models.TextField(blank=True, null=True)
    communication = models.TextField(blank=True, null=True)
    action_comm = models.TextField(blank=True, null=True)
    action_non_conformite = models.TextField(blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "29. QUESTIONNAIRES RDUE"
        # ordering = ["libelle"]
