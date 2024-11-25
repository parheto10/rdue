from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password,check_password


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Utilisateur
        fields=[
            'id',
            'email',
            'nom',
            'prenom',
            'code',
            'tel',
            # 'date_adh_agromap',
            # 'sexe',
            'fonction',
            'is_online',
            'is_active',
            'is_superadmin',
            'is_admin',
            'is_client',
            'is_responsable',
            'is_supervisor',
            'is_gestionnaire',
            'is_adg',
            'is_technicien',
            'is_pepinieriste',
            'password'
        ]
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        # Hash the password before saving it to the database
        validated_data['password'] = make_password(validated_data['password'])
        return super(UtilisateurSerializer, self).create(validated_data)
        
    def __init__(self, *args, **kwargs):
        super(UtilisateurSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1


class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Fournisseur
        fields=[
            'id',
            'code',
            'libelle',
        ]
    def __init__(self, *args, **kwargs):
        super(FournisseurSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Projet
        fields=['id',
                'nomProjet',
                'countrie',
                'description',
                'dateDebut',
                'dateFin',
                'objectif',
                'etat',
                'plant_aproduit',
                'respo',
                'carbon_astock',
                'logo',
                'emp_engageof_proj',
                'total_coop_projet',
                'total_producteurs_projet',
                'total_parcelles_projet',
                'total_parcelles_proj_risk_modere',
                'total_parcelles_proj_risk_zero',
                'total_superficie_projet',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ProjetSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class UserProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserProjet
        fields=['id',
                'utilisateur',
                'projet',
                'etatuser',
        ]
        
    def __init__(self, *args, **kwargs):
        super(UserProjetSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class CategorieEspeceSerialiser(serializers.ModelSerializer):
    class Meta:
        model=models.CategorieEspece
        fields=['id','libelle']
        
class CountrieSerialiser(serializers.ModelSerializer):
    class Meta:
        model=models.Countrie
        fields=['id','libelle','code']
        
        
class EspeceSerialiser(serializers.ModelSerializer):
    class Meta:
        model=models.Espece
        fields=[
            'id',
            'libelle',
            'categorie',
            'accronyme',
            'densite',
            'hmax',
            'dmax',
            'co2_annuel',
            'created_at',
            'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(EspeceSerialiser, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class SimulateCarbonSerialiser(serializers.ModelSerializer):
    class Meta:
        model=models.SimulateCarbon
        fields=[
            'id',
            'anneePeuplement',
            'code',
            'totalCarbone',
            'created_at',
            'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(SimulateCarbonSerialiser, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            

class EspeceSimulateSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.EspeceSimulate
        fields=['id',
                'simulate',
                'espece',
                'quantity',
                'carboneStocke',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(EspeceSimulateSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            

class CampagneSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Campagne
        fields=['id',
                'libelle',
                'dateDebut',
                'DateFin',
                'etat',
                'duree_campagne',
                'respo',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(CampagneSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class CampagneProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CampagneProjet
        fields=['id',
                'campagne',
                'projet'
        ]
        
    def __init__(self, *args, **kwargs):
        super(CampagneProjetSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            
            

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Region
        fields=['id',
                'libelle',
                'countrie',
                'chef_lieu_reg',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(RegionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            

class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Cooperative
        fields=['id',
                'fournisseur',
                'region',
                'respCoop',
                'numConnaissement',
                'numRegistre',
                'projet',
                'nomCoop',
                'contacts',
                'siege',
                'logo',
                'etat',
                'respo',
                'total_producteurs_coop',
                'total_sections_coop',
                'total_parcelles_coop',
                'sumPlantCoop',
                'sumSuperficie',
                'carbonStockeCoop',
                'created_at',
                'updated_at',
                'total_parcelles_coop_risk_eleve',
                'total_parcelles_coop_risk_modere',
                'sumSuperficieRisqueModere',
                'total_parcelles_coop_risk_zero',
                'total_parcelles_a_risque',
                'total_parcelles_sup_4ha',
                'total_parcelles_inf_4ha',
                'sumSuperficieInf4ha',
                'sumSuperficieSup4ha',
                'total_production_coop',
                'get_fournisseur',

                # 'pourcentage_parcelles_sup_4ha',
                # 'pourcentage_parcelles_inf_4ha',
                ]
        
    def __init__(self, *args, **kwargs):
        super(CooperativeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            



class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Section
        fields=[
            'id',
            'cooperative',
            'libelle',
            'created_at',
            'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(SectionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            


class GroupeProducteurSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.GroupeProducteur
        fields=['id',
                'libelle',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(GroupeProducteurSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            

class ProducteurSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Producteur
        fields=['code',
                'section',
                'nomComplet',
                'contacts',
                'photo',
                'nbParc',
                'etat',
                'campagne',
                'lieu_habitation',
                'groupe',
                'representant',
                'nbreMembre',
                'total_parcelle_prod',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ProducteurSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 3
            

class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Culture
        fields=['id',
                'libelle',
                'cooperative',
                'prix_unitaire_culture',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(CultureSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class ModeAcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ModeAcquisition
        fields=['id',
                'libelle',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ModeAcquisitionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Parcelle
        fields=[
            'code',
            'producteur',
            'campagne',
            'latitude',
            'longitude',
            'superficie',
            'annee_acquis',
            'age_parcelle',
            'culture',
            'risque',
            'acquisition',
            'is_mapped',
            'titre_de_propriete',
            'image_du_titre_de_propriete',
            'fichier_de_mappage',
            'created_at',
            'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ParcelleSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 3
            

class PlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Planting
        fields=['code',
                'parcelle',
                'campagne',
                'plant_existant',
                'plant_recus',
                'note_plant_existant',
                'date',
                'total_monitoring',
                'total_espece_plante',
                'detail_planting_see',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(PlantingSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class DetailPlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.DetailPlanting
        fields=['code',
                'planting',
                'espece',
                'plants'
        ]
        
    def __init__(self, *args, **kwargs):
        super(DetailPlantingSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 3
            

class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Monitoring
        fields=['code',
                'planting',
                'taux_reussite',
                'campagne',
                'date',
                'sumPlantEspece',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(MonitoringSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class MonitoringDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MonitoringDetail
        fields=['code',
                'monitoring',
                'espece',
                'plant_denombre',
                'taux_reussite',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(MonitoringDetailSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            
class ObservationMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ObservationMonitoring
        fields=['id',
                'monitoring',
                'observation',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ObservationMonitoringSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            
class ObservationMortaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ObservationMortalite
        fields=['id',
                'libelle',
            ]
        
    def __init__(self, *args, **kwargs):
        super(ObservationMortaliteSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
            
class SaisonRecolteSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SaisonRecolte
        fields=['id',
                'libelle',
                'cooperative'
        ]
        
    def __init__(self, *args, **kwargs):
        super(SaisonRecolteSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class RecolteProducteurSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.RecolteProducteur
        fields=[
            'code',
            'parcelle',
            'campagne',
            'saison',
            'culture',
            'estimation_production',
            'nbre_sacs',
            'poids_total',
            'prix_total',
            'created_at',
            'updated_at', 
            'check_gap',
            'gap',               
        ]
        
    def __init__(self, *args, **kwargs):
        super(RecolteProducteurSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2

class PSESerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Monitoring
        fields=['code',
                'planting',
                'taux_reussite',
                'campagne',
                'date',
                'sumPlantEspece',
                'created_at',
                'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(MonitoringSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2
            

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Certification
        fields=['id',
                'libelle',
                'created_at',
                'updated_at'
            ]
        
    def __init__(self, *args, **kwargs):
        super(CertificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1



############ ANALYSE RDUE #############################################
class RdueSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.RDUE
        # fields = "__all__"
        fields = [
            'id',
            'entite',
            'produits',
            'chaine_appro',
            'pays_origine',
            'fournisseur',
            'zone_arisque',
            'liste_zone',
            'exp_illegale',
            'mesure_preventives',
            'suivi_mesure',
            'efficacite_mesure',
            'communication',
            'action_comm',
            'action_non_conformite',
            'add_le',
        ]


############ ENQUETES #############################################

class AgeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Age
        fields = [
            'libelle'
        ]

    def __init__(self, *args, **kwargs):
        super(AgeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class ThemeEnqueteSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Theme_Enquete
        fields = [
            'libelle'
        ]

    def __init__(self, *args, **kwargs):
        super(ThemeEnqueteSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class ProduitPhytoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Produit_Phyto
        fields = [
            'libelle'
        ]

    def __init__(self, *args, **kwargs):
        super(ProduitPhytoSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class EngraisSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Engrais
        fields = [
            'libelle'
        ]

    def __init__(self, *args, **kwargs):
        super(EngraisSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class EnqueteSocialSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Enquete_Social
        fields = [
            "id",
            "thematique",
            "producteur",
            "nb_epouse",
            "nb_enfant",
            "nb_personne",
            "is_compte_bancaire",
            "is_mobile_money",
            "numero_mobile_money",
            "revenu_moyen",
        ]

    def __init__(self, *args, **kwargs):
        super(EnqueteSocialSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class AgeEnfantSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Age_enfant
        fields = [
            'id',
            'enquete_social',
            'age',
            'nombre_enfant',
        ]

    def __init__(self, *args, **kwargs):
        super(AgeEnfantSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class AgescolariseSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Age_scolarise
        fields = [
            'id',
            'enquete_social',
            'age',
            'nombre_enfant_scolarise',
        ]

    def __init__(self, *args, **kwargs):
        super(AgescolariseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class EnqueteExploitationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Enquete_Exploitation
        fields = [
            'id',
            'thematique',
            'Parcelle',
            'culture_principale',
            'culture_secondaire',
            'is_main_doeuvre_homme',
            'nb_main_doeuvre_homme',
            'salaire_moyen_homme',
            'is_main_doeuvre_femme',
            'nb_main_doeuvre_femme',
            'salaire_moyen_femme',
            'is_produit_phyto',
            'is_engrais',
        ]

    def __init__(self, *args, **kwargs):
        super(EnqueteExploitationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class DetailAgeHommeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Detail_Age_Homme
        fields = [
            'id',
            'enquete_exploitation',
            'age_homme',
            'nombre_homme',
        ]

    def __init__(self, *args, **kwargs):
        super(DetailAgeHommeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class DetailAgeFemmeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Detail_Age_Femme
        fields = [
            'id',
            'enquete_exploitation',
            'age_femme',
            'nombre_femme',
        ]

    def __init__(self, *args, **kwargs):
        super(DetailAgeFemmeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1
class DetailPhytoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Detail_phyto
        fields = [
            'id',
            'enquete_exploitation',
            'produits_phyto',
            'nom_produit',
        ]

    def __init__(self, *args, **kwargs):
        super(DetailPhytoSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class DetailEngraisSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Detail_Engrais
        fields = [
            'id',
            'enquete_exploitation',
            'engrais',
            'nom_engrais',
        ]
    def __init__(self, *args, **kwargs):
        super(DetailEngraisSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1

class ActeProprieteSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Acte_Propriete
        fields = [
            'id',
            'libelle',
        ]
    def __init__(self, *args, **kwargs):
        super(ActeProprieteSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1



class SectionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Section
        fields=[
            'id',
            'cooperative',
            'libelle',
            'created_at',
            'updated_at',
        ]
        
    def __init__(self, *args, **kwargs):
        super(SectionPointSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Point
        fields=[
            'id',
            'section',
            'point_type',
            'libelle',
            'contacts',
            'latitude',
            'longitude',
            'photo',
        ]
    def __init__(self, *args, **kwargs):
        super(PointSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 2






