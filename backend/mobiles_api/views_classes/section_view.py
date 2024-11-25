# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import SectionSerializer
from myapi.models import Cooperative, Section

class SectionViewSet(ViewSet):
    serializer_class = SectionSerializer
    
    @action(detail=False)
    def all_section_by_cooperative(self, request):
        try:
            id_coop = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_coop)
            sections = Section.objects.filter(cooperative=cooperative)
            serializer = self.serializer_class(sections, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Liste des sections de la coopérative {cooperative.nomCoop}', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        
            
        