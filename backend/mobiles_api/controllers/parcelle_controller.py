from django.core.files import File
import json
import simplekml

class ParcelleController:
    
    def json_to_kml(self, fichier_json:File):
        kml_file = simplekml.Kml()
        fichier_json.open('r')
        mapping_json = json.load(fichier_json)
        polygone = [(point[0], point[1]) for point in mapping_json['polygone']]
        
        kml_file.newpolygon(name=f"Code parcelle : {mapping_json['codeParcelle']}", outerboundaryis = polygone)
        return kml_file