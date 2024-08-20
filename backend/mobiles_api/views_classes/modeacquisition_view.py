# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import ModeAcquisitionSerializer
from myapi.models import ModeAcquisition

class ModeAcquisitionViewSet(ViewSet):
    serializer_class = ModeAcquisitionSerializer
    
    @action(detail=False)
    def get_all_mode_acquisition(self, request):
        try:
            modes_acquisition = ModeAcquisition.objects.all()
            serializer = self.serializer_class(modes_acquisition, many=True)
            response = ResponseClass(result=True, has_data=True, message="Liste des modes d'acquisition de parcelle", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()