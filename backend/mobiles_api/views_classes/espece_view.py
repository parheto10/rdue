# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import EspeceSerializer
from myapi.models import Espece

class EspeceViewSet(ViewSet):
    serializer_class = EspeceSerializer
    
    @action(detail=False)
    def get_all_espece(self, request):
        try:
            especes = Espece.objects.all()
            serializer = self.serializer_class(especes, many=True)
            response = ResponseClass(result=True, has_data=True, message='Liste des cultures', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()