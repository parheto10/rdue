from myapi.models import Monitoring, ObservationMonitoring, ObservationMortalite


class ObservationMonitoringController:
    def synchronisation(self, data, monitoring: Monitoring):
        try:
            observation_mortalite = ObservationMortalite.objects.get(pk=data['observation_mortalite_id'])
            observation_monitoring = ObservationMonitoring.objects.create(monitoring = monitoring, observation= observation_mortalite)
            return observation_monitoring
        except Exception as e:
            raise Exception(str(e))