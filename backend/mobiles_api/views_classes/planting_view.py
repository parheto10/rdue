# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import PlantingSerializer
from myapi.models import Planting, Parcelle

class plantingViewSet(ViewSet):
    serializer_class = PlantingSerializer
    
    @action(detail=False)
    def get_planting_by_parcelle(self, request):
        try:
            code_parcelle = self.request.GET.get('code_parcelle')
            parcelle = Parcelle.objects.get(pk=code_parcelle)
            plantings = Planting.objects.filter(parcelle=parcelle)
            serializer = self.serializer_class(plantings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des plantings de la parcelle {parcelle.code}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()