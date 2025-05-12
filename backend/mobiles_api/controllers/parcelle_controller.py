import os
from django.core.files import File
import json
import simplekml

from myapi.models import Acte_Propriete, Campagne, Culture, ModeAcquisition, Parcelle, Producteur

class ParcelleController:
    
    def json_to_kml(self, fichier_json:File):
        kml_file = simplekml.Kml()
        fichier_json.open('r')
        mapping_json = json.load(fichier_json)
        polygone = [(point[0], point[1]) for point in mapping_json['polygone']]
        
        kml_file.newpolygon(name=f"Code parcelle : {mapping_json['codeParcelle']}", outerboundaryis = polygone)
        return kml_file
    
    def synchronisation(self, request)->Parcelle:
        try:
            code = request.data['code']
            # campagne = None if request.data['campagne']== '' else Campagne.objects.get(pk=request.data['campagne'])
            # culture = None if request.data['culture']== '' else Culture.objects.get(pk=request.data['culture'])
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            # superficie = request.data['superficie']
            # annee_acquis = request.data['annee_acquis']
            is_mapped = bool(request.data['is_mapped'])
            # acquisition = None if request.data['acquisition']== '' else ModeAcquisition.objects.get(pk=request.data['acquisition'])
            # titre_de_propriete = None if request.data['titre_de_propriete']=='' else Acte_Propriete.objects.get(pk=request.data['titre_de_propriete'])
            # image_du_titre_de_propriete = None if request.data['image_du_titre_de_propriete']==None else File(request.data['image_du_titre_de_propriete'])
            
            # producteur = Producteur.objects.get(code=request.data['producteur'])
            parcelle, created = Parcelle.objects.get_or_create(code=code)
            # parcelle.producteur = producteur
            # parcelle.campagne = campagne
            parcelle.is_mapped = is_mapped
            # parcelle.culture = culture
            parcelle.latitude = latitude
            parcelle.longitude = longitude
            # parcelle.superficie = superficie
            # parcelle.annee_acquis = annee_acquis
            # parcelle.acquisition = acquisition
            # parcelle.titre_de_propriete = titre_de_propriete
            # parcelle.image_du_titre_de_propriete = image_du_titre_de_propriete
            if request.data['fichier_de_mappage'] != "":
                fichier_de_mappage = self.json_to_kml(File(request.data['fichier_de_mappage']))
                fichier_de_mappage_path = f'{code}.kml'
                fichier_de_mappage.save(fichier_de_mappage_path)
                with open(fichier_de_mappage_path, 'rb') as mapping:
                    parcelle.fichier_de_mappage = File(mapping)
                os.remove(fichier_de_mappage_path)
            parcelle.save()
            return parcelle
        except Exception as e:
            raise Exception(str(e))
