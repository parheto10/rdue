from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from foret.naiveclasses import ResponseClass
from myapi.models import Cooperative, Monitoring, ObservationMonitoring
from mobiles_api.serializers import ObservationMonitoringSerializer

class ObservationMonitoringViewSet(ViewSet):
  class_serializer = ObservationMonitoringSerializer
    
  @action(detail=False)
  def get_all_observation_monitoring_by_cooperative(self, request):
    try:
      id_cooperative = self.request.GET.get('id_cooperative')
      cooperative = Cooperative.objects.get(pk=id_cooperative)
      observation_monitoring = ObservationMonitoring.objects.filter(monitoring__planting__parcelle__producteur__section__cooperative=cooperative)
      serializer = self.class_serializer(observation_monitoring, many=True)
      response = ResponseClass(result=True, has_data=True, message=f'Liste des observations de monitoring ', data=serializer.data)
    except Exception as e:
      response = ResponseClass(result=False, has_data=False, message=str(e))
    finally:
      return response.json_response()
    
  @action(detail=False)
  def get_all_observation_monitoring_by_monitoring(self, request):
    try:
      monitoring = Monitoring.objects.get(code=self.request.GET.get('code_monitoring'))
      observation_monitoring = ObservationMonitoring.objects.filter(monitoring = monitoring)
      serializer = self.class_serializer(observation_monitoring, many=True)
      response = ResponseClass(result=True, has_data=True, message=f'Liste des observations du monitoring {monitoring.code}', data=serializer.data)
    except Exception as e:
      response = ResponseClass(result=False, has_data=False, message=str(e))
    finally:
      return response.json_response()