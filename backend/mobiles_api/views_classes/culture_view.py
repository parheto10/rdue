# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import CultureSerializer
from myapi.models import Culture, Cooperative

class CultureViewSet(ViewSet):
    serializer_class = CultureSerializer
    
    @action(detail=False)
    def get_all_culture_by_cooperative(self, request):
        try:
            id_cooperative = self.request.GET.get('id_cooperative')
            cooperative = Cooperative.objects.get(pk=id_cooperative)
            cultures = Culture.objects.filter(cooperative=cooperative)
            serializer = self.serializer_class(cultures, many=True)
            response = ResponseClass(result=True, has_data=True, message='Liste des cultures', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()