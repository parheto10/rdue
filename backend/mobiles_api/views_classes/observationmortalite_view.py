# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ObservationMortaliteSerializer
from myapi.models import ObservationMortalite

class ObservationMortaliteViewSet(ViewSet):
    serializer_class = ObservationMortaliteSerializer
    
    @action(detail=False)
    def get_all_observation_mortalite(self, request):
        try:
            observation_mortalite = ObservationMortalite.objects.all()
            serializer = self.serializer_class(observation_mortalite, many=True)
            response = ResponseClass(result=True, has_data=True, message='Liste des observations de mortalité', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()