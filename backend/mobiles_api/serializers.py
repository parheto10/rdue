from rest_framework.serializers import ModelSerializer

# models imports
from myapi.models import Cooperative, Utilisateur, Section, Campagne, Producteur, Parcelle, Planting, DetailPlanting

class UtilisateurSerializer(ModelSerializer):
    
    class Meta:
        model = Utilisateur
        fields = ['id','nom', 'prenom', 'tel', 'password', 'sexe']
        read_only = ['id','nom', 'prenom', 'tel', 'password', 'sexe']
        
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