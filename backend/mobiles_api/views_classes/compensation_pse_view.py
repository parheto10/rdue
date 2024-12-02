# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from mobiles_api.models import CompensationPSE
from mobiles_api.serializers import CompensationPSESerializer
from foret.naiveclasses import ResponseClass

class CompensationPSEViewSet(ViewSet):
    serializer_class = CompensationPSESerializer
    
    @action(detail=False, methods=['post'])
    def insert(self, request):
        try:
            code = request.data['code']
            libelle = request.data['libelle']
            compensation = CompensationPSE.objects.create(code = code, libelle = libelle)
            response = ResponseClass(result=True, has_data=False, message=f"Insertion de {compensation.libelle}")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
       
    @action(detail=False)
    def compensation_pse_list(self, request):
        try:
            compensations = CompensationPSE.objects.all()
            serializer = self.serializer_class(compensations, many=True)
            response = ResponseClass(result=True, has_data=True, message=f"Liste des compensations", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()