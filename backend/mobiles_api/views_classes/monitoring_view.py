# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.controllers.observationmonitoring_controller import ObservationMonitoringController
from myapi.models import Cooperative, Monitoring, Planting
from foret.naiveclasses import ResponseClass
from mobiles_api.controllers.monitoring_controller import MonitoringController
from mobiles_api.controllers.detailmonitoring_controller import DetailMonitoringController
from mobiles_api.serializers import MonitoringSerializer
from mobiles_api.models import InfoPSE

class MonitoringViewSet (ViewSet):
    serializer_class = MonitoringSerializer
    monitoring_controller = MonitoringController()
    detail_monitoring_controller = DetailMonitoringController()
    observation_monitoring_controller = ObservationMonitoringController()
    
    @action(detail=False)
    def get_all_monitoring_by_planting(self, request):
        try:
            code_planting = self.request.GET.get('code_planting')
            planting = Planting.objects.get(pk=code_planting)
            monitorings = Monitoring.objects.filter(planting=planting)
            serializer = self.serializer_class(monitorings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des monitorings du planting {planting.code}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False)
    def get_all_monitoring_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            monitorings = Monitoring.objects.filter(planting__parcelle__producteur__section__cooperative=cooperative)
            serializer = self.serializer_class(monitorings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des monitorings de la cooperative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
        
    @action(detail=False)
    def get_all_monitoring_by_info_pse(self, request):
        try:
            id_info_pse = self.request.GET.get('id_info_pse')
            info_pse = InfoPSE.objects.get(pk=id_info_pse)
            monitorings = Monitoring.objects.filter(planting__parcelle__producteur__section__cooperative__projet = info_pse.projet, campagne = info_pse.campagne)
            serializer = self.serializer_class(monitorings, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des monitorings du PSE {info_pse.projet.nomProjet}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
        
    @action(detail=False, methods=['post'])
    def synchronisation(self, request):
        try:
            detail_monitoring = []
            observation_monitoring = []
            monitoring = self.monitoring_controller.synchronisation(request)
            observations = request.data['observations']
            details = request.data['details']
            if monitoring is not None:
                for detail in details:
                    detail_monitoring.append(self.detail_monitoring_controller.synchronisation(detail, monitoring=monitoring))
                    
                for observation in observations:
                    observation_monitoring.append(self.observation_monitoring_controller.synchronisation(observation, monitoring=monitoring))
                    
            response = ResponseClass(result=True, has_data=False, message=f'Synchronisation du monitoring {monitoring.code} réussie avec {len(detail_monitoring)} détails et {len(observation_monitoring)} observations')
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()