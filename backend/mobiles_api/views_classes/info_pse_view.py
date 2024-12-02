# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from myapi.models import Projet, Campagne
from mobiles_api.models import ActiviteRetribution, InfoPSE, CompensationPSE
from mobiles_api.serializers import InfoPSESerializer
from foret.naiveclasses import ResponseClass

class InfoPSEViewSet(ViewSet):
    serializer_class = InfoPSESerializer
    
    @action(detail=False, methods=['post'])
    def insert(self, request):
        activites = []
        try:
            pourcentage_retribution = request.data['pourcentage_retribution']
            montant_pse = request.data['montant_pse']
            compensation = CompensationPSE.objects.get(pk = request.data['id_compensation'])
            projet = Projet.objects.get(pk = request.data['id_projet'])
            campagne = Campagne.objects.get(pk = request.data['id_campagne'])
            infos = InfoPSE.objects.create(pourcentage_retribution = pourcentage_retribution, montant_pse = montant_pse, compensation = compensation, projet = projet, campagne = campagne)
            for id_activite in request.data['activites']:
                activite = ActiviteRetribution.objects.get(pk=id_activite["id_activite"])
                infos.activites.add(activite)
            response = ResponseClass(result=True, has_data=False, message="Enregistré avec succès")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    
    @action(detail=False)
    def info_pse_list(self, request):
        try:
            infos = InfoPSE.objects.all()
            serializer = self.serializer_class(infos, many=True)
            response = ResponseClass(result=True, has_data=False, message="Liste des infos PSE", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False)
    def info_pse_list_by_projet(self, request):
        try:
            id_projet = request.GET.get('id_projet')
            projet = Projet.objects.get(pk = id_projet)
            infos = InfoPSE.objects.filter(projet = projet)
            serializer = self.serializer_class(infos, many=True)
            response = ResponseClass(result=True, has_data=False, message="Liste des infos PSE", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        