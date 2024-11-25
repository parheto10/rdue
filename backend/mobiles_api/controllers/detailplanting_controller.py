import uuid
from myapi.models import DetailPlanting, Espece, Planting


class DetailPlantingController:
    def synchronisation(self, data, planting:Planting):
        try:
            code = f'DPL-{uuid.uuid4().hex.upper()[0:10]}'
            plants = data['plants']
            espece = None if data['espece'] ==None else Espece.objects.get(id=data['espece'])
            detailPlanting, created = DetailPlanting.objects.get_or_create(code=code)
            detailPlanting.plants = plants
            detailPlanting.espece = espece
            detailPlanting.planting = planting
            detailPlanting.save()
            return detailPlanting
        except Exception as e:
            None
        