from decimal import Decimal
import uuid
from myapi.models import DetailPlanting, Espece, Monitoring, MonitoringDetail


class DetailMonitoringController:
    def synchronisation(self, data, monitoring:Monitoring):
        try:
            code = f'DMN-{uuid.uuid4().hex.upper()[0:10]}'
            espece = None if data['espece'] ==None else Espece.objects.get(id=data['espece'])
            plant_denombre = data['plant_denombre']
            taux_reussite = Decimal(data['taux_reussite'])
            detailMonitoring, created = MonitoringDetail.objects.get_or_create(code=code)
            detailMonitoring.monitoring = monitoring
            detailMonitoring.espece = espece
            detailMonitoring.plant_denombre = plant_denombre
            detailMonitoring.taux_reussite = taux_reussite
            detailMonitoring.save()
            return detailMonitoring
        except Exception as e:
            None
        