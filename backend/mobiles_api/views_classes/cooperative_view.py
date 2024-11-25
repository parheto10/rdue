# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.models import Technicien
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import CooperativeSerializer
from myapi.models import Cooperative

class CooperativeViewSet(ViewSet):
    
    model = Cooperative
    serializer_class = CooperativeSerializer
    
    @action(detail=False)
    def get_cooperative(self, request):
        try:
            tel = self.request.GET.get('technicien_tel')
            technicien = Technicien.objects.get(user__tel=tel)
            serializer = self.serializer_class(technicien.cooperative, many=False)
            response = ResponseClass(result=True, has_data=True, message=f'Coopérative {technicien.cooperative.nomCoop}', data=serializer.data)
        except Technicien.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()
       
        
    