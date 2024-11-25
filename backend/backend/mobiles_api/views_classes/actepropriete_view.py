# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ActeProprieteSerializer
from myapi.models import Acte_Propriete

class ActeProprieteViewSet(ViewSet):
    serializer_class = ActeProprieteSerializer
    
    @action(detail=False)
    def get_all_acte_propriete(self, request):
        try:
            actes_propriete = Acte_Propriete.objects.exclude(libelle='AUCUN')
            serializer = self.serializer_class(actes_propriete, many=True)
            response = ResponseClass(result=True, has_data=True, message="Liste des actes de propriété", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()