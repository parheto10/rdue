# Externals imports
import random
import uuid
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import DetailMonitoringSerializer
from myapi.models import Cooperative, Monitoring, MonitoringDetail

class DetailMonitoringViewSet(ViewSet):
    
    serializer_class = DetailMonitoringSerializer
    
    @action(detail=False)
    def get_all_details_monitorings_by_monitoring(self, request):
        try:
            code_monitoring = self.request.GET.get('code_monitoring')
            monitoring = Monitoring.objects.get(pk=code_monitoring)
            details_monitoring = MonitoringDetail.objects.filter(monitoring=monitoring)
            serializer = self.serializer_class(details_monitoring, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des détails du monitoring {monitoring.code}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False)
    def get_all_details_monitorings_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            details_monitoring = MonitoringDetail.objects.filter(monitoring__planting__parcelle__producteur__section__cooperative=cooperative).exclude(plant_denombre=0)
            serializer = self.serializer_class(details_monitoring, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des détails de monitoring de la coopérative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()