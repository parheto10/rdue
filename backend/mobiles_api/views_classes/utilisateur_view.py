from django.contrib.auth.hashers import check_password
# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import UtilisateurSerializer
from myapi.models import Utilisateur

class UtilisateurViewSet(ViewSet):
    
    serializer_class = UtilisateurSerializer
    
    @action(detail=False, methods=['POST'])
    def connexion(self, request):
        tel = request.data['tel']
        password = request.data['password']
        try:
            user = Utilisateur.objects.get(tel=tel)
            if user.is_technicien:
                if check_password(password, user.password):
                    serializer = self.serializer_class(user, many=False)
                    response = ResponseClass(result=True, has_data=True, message="Connexion réussie", data=serializer.data)
                else:
                    response = ResponseClass(result=False, has_data=False, message="Mot de passe erroné.")
            else:
                response = ResponseClass(result=False, has_data=False, message="Vous n'êtes pas autorisés à vous connecter à cette application.")
        except Utilisateur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce numéro de téléphone n'existe pas ou est erroné.")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
        