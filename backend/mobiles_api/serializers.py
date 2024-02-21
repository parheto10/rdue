from rest_framework.serializers import ModelSerializer

# models imports
from myapi.models import Utilisateur

class UtilisateurSerializer(ModelSerializer):
    
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'tel', 'password', 'sexe']
        read_only = ['nom', 'prenom', 'tel', 'password', 'sexe']