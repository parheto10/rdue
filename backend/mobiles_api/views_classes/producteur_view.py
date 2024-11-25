# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ProducteurSerializer
from myapi.models import Campagne, Producteur, Cooperative, Section

class ProducteurViewSet(ViewSet):
    
    serializer_class = ProducteurSerializer
    
    @action(detail=False)
    def get_all_producteur_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            producteurs = Producteur.objects.filter(section__cooperative=cooperative)
            serializer = self.serializer_class(producteurs, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des producteurs de la coopérative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
    @action(detail=False, methods=['post'])
    def synchronisation(self, request):
        try:
            code = request.data['code']
            section = Section.objects.get(pk=request.data['section'])
            campagne = None if request.data['campagne']==None else Campagne.objects.get(pk=request.data['campagne'])
            nomComplet = request.data['nomComplet']
            contacts = request.data['contacts']
            nbParc = request.data['nbParc']
            lieu_habitation = request.data['lieu_habitation']
            producteur, created = Producteur.objects.get_or_create(code=code)
            producteur.section=section
            producteur.campagne = campagne
            producteur.nomComplet=nomComplet
            producteur.contacts=contacts
            producteur.nbParc=nbParc
            producteur.lieu_habitation=lieu_habitation
            producteur.save()
            response = ResponseClass(result=True, has_data=False, message='')
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()