# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.models import CategorieActiviteRetribution, ActiviteRetribution
from mobiles_api.serializers import CategorieActiviteRetributionSerializer, ActiviteRetributionSerializer
from foret.naiveclasses import ResponseClass

class CategorieActiviteRetributionViewSet(ViewSet):
    serializer_class = CategorieActiviteRetributionSerializer
    
    @action(detail=False, methods=['post'])
    def insert(self, request):
        try:
            libelle = request.data['libelle']
            categorie = CategorieActiviteRetribution.objects.create(libelle = libelle)
            response = ResponseClass(result=True, has_data=False, message=f"Insertion de {categorie.libelle}")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
       
    @action(detail=False)
    def categorie_activite_retribution_list(self, request):
        try:
            categories = CategorieActiviteRetribution.objects.all()
            serializer = self.serializer_class(categories, many=True)
            response = ResponseClass(result=True, has_data=True, message=f"Liste des catégories", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
class ActiviteRetributionViewSet(ViewSet):
    serializer_class = ActiviteRetributionSerializer
    
    @action(detail=False, methods=['post'])
    def insert(self, request):
        try:
            libelle = request.data['libelle']
            id_categorie = request.data['id_categorie']
            activite = ActiviteRetribution.objects.create(libelle = libelle, categorie = CategorieActiviteRetribution.objects.get(pk=id_categorie))
            response = ResponseClass(result=True, has_data=False, message=f"Insertion de {activite.libelle}")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
       
    @action(detail=False)
    def activite_retribution_list(self, request):
        try:
            activites = ActiviteRetribution.objects.all()
            serializer = self.serializer_class(activites, many=True)
            response = ResponseClass(result=True, has_data=True, message=f"Liste des activités", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()