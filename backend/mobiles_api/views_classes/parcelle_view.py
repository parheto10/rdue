# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ParcelleSerializer
from myapi.models import Parcelle, Producteur

class ParcelleViewSet(ViewSet):
    
    serializer_class = ParcelleSerializer
    
    @action(detail=False)
    def get_all_parcelle_by_producteur(self, request):
        try:
            code_producteur = self.request.GET.get('code_producteur')
            producteur = Producteur.objects.get(pk=code_producteur)
            parcelles = Parcelle.objects.filter(producteur=producteur)
            serializer = self.serializer_class(parcelles, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des parcelles de {producteur.nomComplet}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    