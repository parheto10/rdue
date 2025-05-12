from datetime import datetime
import uuid
from myapi.models import Campagne, Espece, Parcelle, Planting


class PlantingController:
    def synchronisation(self, request):
        try:
            code = f"PLG-{uuid.uuid4().hex.upper()[0:10]}"
            campagne = None if request.data['campagne']==None else Campagne.objects.get(pk=request.data['campagne'])
            plant_existant = request.data['plant_existant']
            plant_recus = int(request.data['plant_recus'])
            note_plant_existant = request.data['note_plant_existant']
            date = datetime.fromisoformat(request.data['date'])
            parcelle = None if request.data['parcelle']==None else Parcelle.objects.get(pk=request.data['parcelle'])
            planting, created = Planting.objects.get_or_create(code=code)
            planting.latitude_du_lieu_de_planting = request.data['latitude_du_lieu_du_planting']
            planting.longitude_du_lieu_de_planting = request.data['longitude_du_lieu_du_planting']
            planting.campagne = campagne
            planting.plant_existant = plant_existant
            planting.plant_recus = plant_recus
            planting.note_plant_existant = note_plant_existant
            planting.date = date
            planting.parcelle = parcelle
            planting.save()
            return planting
        except Exception as e:
            raise Exception(str(e))
