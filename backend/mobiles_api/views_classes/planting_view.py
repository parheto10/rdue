from datetime import datetime
import uuid
# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.controllers.planting_controller import PlantingController
from mobiles_api.controllers.detailplanting_controller import DetailPlantingController
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import PlantingSerializer
from myapi.models import Campagne, Planting, Parcelle, Cooperative

class plantingViewSet(ViewSet):
    serializer_class = PlantingSerializer
    planting_controller = PlantingController()
    detail_planting_controller = DetailPlantingController()
    @action(detail=False)
    def get_all_planting_by_parcelle(self, request):
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
        
    @action(detail=False)
    def get_all_planting_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            plantings = Planting.objects.filter(parcelle__producteur__section__cooperative=cooperative).exclude(date=None, plant_recus=0)
            serializer = self.serializer_class(plantings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des plantings de la cooperative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False, methods=['post'])
    def synchronisation(self, request):
        try:
            detail_planting = []
            planting = self.planting_controller.synchronisation(request)
            details = request.data['details']
            if planting is not None:
                for detail in details:
                    detail_planting.append(self.detail_planting_controller.synchronisation(detail, planting=planting))
            response = ResponseClass(result=True, has_data=False, message=str(detail_planting))
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()