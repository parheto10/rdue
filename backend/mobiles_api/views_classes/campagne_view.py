# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import CampagneSerializer
from myapi.models import Campagne

class CampagneViewSet(ViewSet):
    
    serializer_class = CampagneSerializer
    
    @action(detail=False)
    def get_all_active_campagne(self, request):
        try:
            campagnes = Campagne.objects.filter(etat=True)
            serializer = self.serializer_class(campagnes, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des campagnes actives', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    