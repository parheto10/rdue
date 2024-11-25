from rest_framework.serializers import ModelSerializer

# models imports
# from myapi.models import Acte_Propriete, Cooperative, Utilisateur, Section, Campagne, Producteur, Parcelle, Planting, DetailPlanting, Certification, Culture, ModeAcquisition, Espece
from .models import Certificat
from myapi.models import Utilisateur, Cooperative, Section, Campagne, Producteur, Parcelle, Planting, DetailPlanting, Espece, Certification, Culture, ModeAcquisition, Acte_Propriete


class UtilisateurSerializer(ModelSerializer):
    
    class Meta:
        model = Utilisateur
        fields = ['id','nom', 'prenom', 'tel', 'sexe']
        read_only = ['id','nom', 'prenom', 'tel', 'sexe']
        
class CooperativeSerializer(ModelSerializer):
    
    class Meta:
        model = Cooperative
        fields = '__all__'
        
class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        exclude = ['cooperative']
        
class CampagneSerializer(ModelSerializer):
    class Meta:
        model = Campagne
        fields = '__all__'
        
class ProducteurSerializer(ModelSerializer):
    
    class Meta:
        model = Producteur
        fields = '__all__'
        
class ParcelleSerializer(ModelSerializer):
    
    class Meta:
        model = Parcelle
        fields = '__all__'
        
class PlantingSerializer(ModelSerializer):
    
    class Meta:
        model = Planting
        fields = '__all__'
        

class DetailPlantingSerializer(ModelSerializer):
    
    class Meta:
        model = DetailPlanting
        fields = '__all__'
        
class EspeceSerializer(ModelSerializer):
    
    class Meta:
        model = Espece
        fields = '__all__'
        

class CertificationSerializer(ModelSerializer):
    
    class Meta:
        model = Certification
        fields = ['id', 'libelle']
        
class CertificatSerializer(ModelSerializer):
    
    class Meta:
        model = Certificat
        fields = '__all__'
        

class CultureSerializer(ModelSerializer):
    
    class Meta:
        model = Culture
        fields = ['id', 'libelle']
        

class ModeAcquisitionSerializer(ModelSerializer):
    
    class Meta:
        model = ModeAcquisition
        fields = ['id', 'libelle']
        
class ActeProprieteSerializer(ModelSerializer):
    
    class Meta:
        model = Acte_Propriete
        fields = ['id', 'libelle']