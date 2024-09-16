from decimal import Decimal
import uuid
from datetime import datetime

from myapi.models import Campagne, Planting, Monitoring


class MonitoringController :
    def synchronisation(self, request):
        try:
            code = f"MNT-{uuid.uuid4().hex.upper()[0:10]}"
            planting = Planting.objects.get(pk=request.data['planting'])
            date  = datetime.fromisoformat(request.data['date'])
            taux_reussite = Decimal(request.data['taux_reussite'])
            campagne = None if request.data['campagne']==None else Campagne.objects.get(pk=request.data['campagne'])
            
            monitoring, created = Monitoring.objects.get_or_create(code=code)
            monitoring.planting = planting
            monitoring.date = date
            monitoring.taux_reussite = taux_reussite
            monitoring.campagne = campagne
            monitoring.save()
            return monitoring
        except Exception as e:
            None