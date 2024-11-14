from django.core.files import File
import os
import json

# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.controllers.certification_controller import CertificationController
from mobiles_api.controllers.parcelle_controller import ParcelleController
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ParcelleSerializer
from myapi.models import  Parcelle, Producteur, Cooperative

class ParcelleViewSet(ViewSet):
    
    serializer_class = ParcelleSerializer
    controller_class = ParcelleController()
    certification_controller_class = CertificationController()
    
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
            details = json.loads(request.data['certificats'])
            parcelle = self.controller_class.synchronisation(request)
            if parcelle is not None:
                for certif in details:
                    self.certification_controller_class.synchronisation(certif, parcelle=parcelle)
            response = ResponseClass(result=True, has_data=False, message=f'Synchronisation de la parcelle {parcelle.code} réussie ')
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()