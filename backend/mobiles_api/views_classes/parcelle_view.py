from django.core.files import File
import os

# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.controllers.parcelle_controller import ParcelleController
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ParcelleSerializer
from myapi.models import Acte_Propriete, Campagne, Culture, ModeAcquisition, Parcelle, Producteur, Cooperative

class ParcelleViewSet(ViewSet):
    
    serializer_class = ParcelleSerializer
    controller_class = ParcelleController()
    
    @action(detail=False)
    def get_all_parcelle_by_producteur(self, request):
        try:
            code_producteur = self.request.GET.get('code_producteur')
            producteur = Producteur.objects.get(pk=code_producteur)
            parcelles = Parcelle.objects.filter(producteur=producteur)
            serializer = self.serializer_class(parcelles, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des parcelles de {producteur.nomComplet}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False)
    def get_all_parcelle_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            parcelles = Parcelle.objects.filter(producteur__section__cooperative=cooperative)
            serializer = self.serializer_class(parcelles, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des parcelles de la coopérative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()

    @action(detail=False, methods=['post'])
    def synchronisation(self, request):
        try:
            code = request.data['code']
            campagne = None if request.data['campagne']== '' else Campagne.objects.get(pk=request.data['campagne'])
            culture = None if request.data['culture']== '' else Culture.objects.get(pk=request.data['culture'])
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            superficie = request.data['superficie']
            annee_acquis = request.data['annee_acquis']
            is_mapped = bool(request.data['is_mapped'])
            acquisition = None if request.data['acquisition']== '' else ModeAcquisition.objects.get(pk=request.data['acquisition'])
            titre_de_propriete = None if request.data['titre_de_propriete']=='' else Acte_Propriete.objects.get(pk=request.data['titre_de_propriete'])
            image_du_titre_de_propriete = None if request.data['image_du_titre_de_propriete']==None else File(request.data['image_du_titre_de_propriete'])
            fichier_de_mappage = self.controller_class.json_to_kml(File(request.data['fichier_de_mappage']))
            fichier_de_mappage_path = f'{code}.kml'
            fichier_de_mappage.save(fichier_de_mappage_path)
            producteur = Producteur.objects.get(code=request.data['producteur'])
            parcelle, created = Parcelle.objects.get_or_create(code=code)
            parcelle.producteur = producteur
            parcelle.campagne = campagne
            parcelle.is_mapped = is_mapped
            parcelle.culture = culture
            parcelle.latitude = latitude
            parcelle.longitude = longitude
            parcelle.superficie = superficie
            parcelle.annee_acquis = annee_acquis
            parcelle.acquisition = acquisition
            parcelle.titre_de_propriete = titre_de_propriete
            parcelle.image_du_titre_de_propriete = image_du_titre_de_propriete
            with open(fichier_de_mappage_path, 'rb') as mapping:
                parcelle.fichier_de_mappage = File(mapping)
                parcelle.save()
            os.remove(fichier_de_mappage_path)
            parcelle.save()
            response = ResponseClass(result=True, has_data=False, message='')
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()