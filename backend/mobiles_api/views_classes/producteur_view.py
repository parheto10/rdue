# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ProducteurSerializer
from myapi.models import Producteur, Cooperative

class ProducteurViewSet(ViewSet):
    
    serializer_class = ProducteurSerializer
    
    @action(detail=False)
    def get_all_producteur_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            producteurs = Producteur.objects.filter(section__cooperative=cooperative)
            serializer = self.serializer_class(producteurs, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des producteurs de la coopérative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()