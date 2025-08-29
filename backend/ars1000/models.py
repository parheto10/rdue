from django.db import models
from myapi.models import Cooperative, Planting, Producteur, Parcelle, Culture, Campagne, CategorieEspece, Espece, Section

class AbstractClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class InformationCooperative(AbstractClass):
    code_cooperative = models.CharField(max_length=255, null=True)
    statut = models.FileField(upload_to='documents/coops', null=True)
    pv_assemblee = models.FileField(upload_to='documents/coops', null=True)
    liste_membres = models.FileField(upload_to='documents/coops', null=True)
    numero_compte_contribuable = models.CharField(max_length=255, null=True)
    numero_cnps = models.CharField(max_length=255, null=True)
    numero_aggrement = models.CharField(max_length=255, null=True)
    immatriculation_ccc = models.CharField(max_length=255, null=True)
    existence_discrimination = models.BooleanField(null=True)
    conformite_ohada = models.BooleanField(null=True)
    cooperative = models.OneToOneField(Cooperative, on_delete=models.CASCADE)


###### Menage du producteur
class CategorieEthnique(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class StatutMatrimonial(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class InfoProducteur(AbstractClass):
    producteur = models.OneToOneField(Producteur, on_delete=models.CASCADE)
    numero_ccc = models.CharField(max_length=255, null=True)
    statut_matrimonial = models.ForeignKey(StatutMatrimonial, on_delete=models.CASCADE)
    categorie_ethnique = models.ForeignKey(CategorieEthnique, on_delete=models.CASCADE)

class StatutMenage(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class Conjoint(AbstractClass):
    code = models.CharField(max_length=255, null=True)
    nom_prenoms = models.CharField(max_length=255, null=True)
    categorie = models.CharField(max_length=255, null=True)
    producteur = models.ForeignKey(InfoProducteur, on_delete=models.CASCADE)

class Enfant(AbstractClass):
    code = models.CharField(max_length=255, null=True)
    nom_prenoms = models.CharField(max_length=255, null=True)
    date_naissance = models.DateField(null=True)
    sexe = models.CharField(max_length=1, null=True)
    statut_scolaire = models.CharField(max_length=255, null=True)
    producteur = models.ForeignKey(InfoProducteur, on_delete=models.CASCADE)
    conjoint = models.ForeignKey(Conjoint, on_delete=models.CASCADE)

class TypeScolarite(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class Scolarite(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)
    type_scolarite = models.ForeignKey(TypeScolarite, on_delete=models.CASCADE)

class EnfantScolarite(AbstractClass):
    enfant = models.ForeignKey(Enfant, on_delete=models.CASCADE)
    scolarite = models.ForeignKey(Scolarite, on_delete=models.CASCADE)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)

###### Tâches Champêtres
class TypeTachesChampetre(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class TacheChampetre(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)
    type_taches_champetre = models.ForeignKey(TypeTachesChampetre, on_delete=models.CASCADE)

class InfoParcelle(AbstractClass):
    precedent_cultural = models.CharField(max_length=255, null=True)
    origine_materiel = models.CharField(max_length=255, null=True)
    # le_champ_est_en_production = models.BooleanField(null=True)
    parcelle = models.OneToOneField(Parcelle, on_delete=models.CASCADE)

class DocumentationFonciere(AbstractClass):
    organe_delivrance = models.CharField(max_length=255, null=True)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    statut_producteur = models.ForeignKey(StatutMenage, on_delete=models.CASCADE)

class EnfantHasTacheChampetre(AbstractClass):
    enfant = models.ForeignKey(Enfant, on_delete=models.CASCADE)
    tache_champetre = models.ForeignKey(TacheChampetre, on_delete=models.CASCADE)
    parcelle = models.ForeignKey(InfoParcelle, on_delete=models.CASCADE)

class IndicateurRisqueTacheChampetre(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetre(AbstractClass):
    enfant_has_tache_champetre = models.ForeignKey(EnfantHasTacheChampetre, on_delete=models.CASCADE)
    indicateur_risque_tache_champetre = models.ForeignKey(IndicateurRisqueTacheChampetre, on_delete=models.CASCADE)

class TypeActionMesureAttenuationTacheChampetre(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class MesureAttenuationTacheChampetre(AbstractClass):
    date = models.DateField(null=True)
    type_action_mesure_attenuation_tache_champetre = models.ForeignKey(TypeActionMesureAttenuationTacheChampetre, on_delete=models.CASCADE)
    cible = models.CharField(max_length=255, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    localite = models.CharField(max_length=255, null=True)
    motifs = models.ManyToManyField(EnfantHasTacheChampetre)

# class DetailMesureAttenuationTacheChampetreFormation(AbstractClass):
#     formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
#     mesure_attenuation_tache_champetre = models.ForeignKey(MesureAttenuationTacheChampetre, on_delete=models.CASCADE)


###### Environnement - Agroforesterie
class Favorabilite(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class AvantageCultureEspece(AbstractClass):
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    favorabilite = models.ForeignKey(Favorabilite, on_delete=models.CASCADE)

class Abattage(AbstractClass):
    code = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)

class DetailAbattage(AbstractClass):
    nbre_plant = models.IntegerField(null=True)
    abattage = models.ForeignKey(Abattage, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE)

class TypeMesureAttenuationAgroforesterie(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class MesureAttenuationAgroforesterie(AbstractClass):
    cible = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)
    type_mesure_attenuation_agroforesterie = models.ForeignKey(TypeMesureAttenuationAgroforesterie, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class DetailMesureAttenuationAgroforesterieAbattage(AbstractClass):
    abattage = models.ForeignKey(Abattage, on_delete=models.CASCADE)
    mesure_attenuation_agroforesterie = models.ForeignKey(MesureAttenuationAgroforesterie, on_delete=models.CASCADE)

class DetailMesureAttenuationAgroforesteriePlanting(AbstractClass):
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)
    mesure_attenuation_agroforesterie = models.ForeignKey(MesureAttenuationAgroforesterie, on_delete=models.CASCADE)

###### Environnement - Phytosanitaire

class CategorieProduit(AbstractClass):
    """Catégorie de produit (Chimique ou biologique)"""
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, null=True)

class TypeProduit(AbstractClass):
    """Type de produit (Insecticide, fongicide, herbicide, etc.)"""
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, null=True)

class Produit(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)
    est_homologue = models.BooleanField(null=True)
    categorie_produit = models.ForeignKey(CategorieProduit, on_delete=models.CASCADE)
    type_produit = models.ForeignKey(TypeProduit, on_delete=models.CASCADE)

class ProduitHasProducteur(AbstractClass):
    produits = models.ManyToManyField(Produit)
    producteur = models.ForeignKey(Producteur, on_delete=models.CASCADE)
    date_de_livraison = models.DateField(null=True)
    cooperative = models.CharField(max_length=255, null=True)

class ParcelleHasProduit(AbstractClass):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_application = models.DateField(null=True)
    dose_par_ha = models.FloatField(null=True)
    applicateur = models.CharField(max_length=255, null=True)
    utilisation_epi = models.BooleanField(null=True)

class TypeActionMesureAttenuationPhyto(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)

class MesureAttenuationPhyto(AbstractClass):
    date = models.DateField(null=True)
    motifs = models.ManyToManyField(ParcelleHasProduit)
    type_mesure_attenuation_phyto = models.ForeignKey(TypeActionMesureAttenuationPhyto, on_delete=models.CASCADE)
    cible = models.CharField(max_length=255, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

###### Légalité & Système de management
class Organigramme(AbstractClass):
    nom_prenoms = models.CharField(max_length=255, null=True)
    competence = models.CharField(max_length=255, null=True)
    poste = models.CharField(max_length=255, null=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

class PlanningAnnuel(AbstractClass):
    document = models.FileField(upload_to='documents/coops', null=True)
    campagne = models.CharField(max_length=255, null=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

class ActionMenee(AbstractClass):
    libelle = models.CharField(max_length=255, null=True)
    ressources_dispo = models.CharField(max_length=255, null=True)
    analyse_swot = models.CharField(max_length=255, null=True)
    besoin_financier = models.IntegerField(null=True)
    date = models.DateField(null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)

class RapportAuditInterne(AbstractClass):
    nom_prenoms_auditeur = models.CharField(max_length=255, null=True)
    rapport_audit = models.FileField(upload_to='documents/coops', null=True)
    liste_des_audites = models.FileField(upload_to='documents/coops', null=True)
    plan_action_correctif = models.FileField(upload_to='documents/coops', null=True)
    fiche_non_conformite = models.FileField(upload_to='documents/coops', null=True)
    date_enregistrement = models.DateField(null=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)