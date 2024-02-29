# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import DetailPlantingSerializer
from myapi.models import Planting, DetailPlanting, Cooperative

class DetailPlantingViewSet(ViewSet):
    
    serializer_class = DetailPlantingSerializer
    
    @action(detail=False)
    def get_all_details_plantings_by_planting(self, request):
        try:
            code_planting = self.request.GET.get('code_planting')
            planting = Planting.objects.get(pk=code_planting)
            details_plantings = DetailPlanting.objects.filter(planting=planting)
            serializer = self.serializer_class(details_plantings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des détails du planting {planting.code}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False)
    def get_all_details_plantings_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            details_plantings = DetailPlanting.objects.filter(planting__parcelle__producteur__section__cooperative=cooperative)
            serializer = self.serializer_class(details_plantings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des détails de planting de la coopérative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()