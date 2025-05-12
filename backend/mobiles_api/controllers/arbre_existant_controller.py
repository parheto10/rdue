from mobiles_api.models import ArbreExistant
from myapi.models import Espece, Parcelle
import base64
from django.core.files.base import ContentFile
from django.core.files import File

class ArbreExistantController:
    def synchronisation(self, data, parcelle:Parcelle):
        try:
            nbre_de_regeneration_naturelle = data['nbre_de_regeneration_naturelle']
            nbre_de_regeneration_assistee = data['nbre_de_regeneration_assistee']
            nbre_plantee = data['nbre_plantee']
            espece = None if data['espece']==None else Espece.objects.get(pk=data['espece'])
            
            arbre_existant, created = ArbreExistant.objects.get_or_create(espece=espece, parcelle=parcelle)
            arbre_existant.nbre_de_regeneration_naturelle = nbre_de_regeneration_naturelle
            arbre_existant.nbre_de_regeneration_assistee = nbre_de_regeneration_assistee
            arbre_existant.nbre_plantee = nbre_plantee
            if data['picture_path'] is not None:
                picture_base64 = base64.b64decode(data['picture_path'])
                picture_converted = ContentFile(picture_base64, name=f"{espece.libelle}.png")
                arbre_existant.picture = picture_converted
            arbre_existant.save()
            return arbre_existant
        except Exception as e:
            raise Exception(str(e))