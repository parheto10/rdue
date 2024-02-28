# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import CertificationSerializer
from myapi.models import Certification

class CertificationViewSet(ViewSet):
    serializer_class = CertificationSerializer
    
    @action(detail=False)
    def get_all_certification(self, request):
        try:
            certifications = Certification.objects.all()
            serializer = self.serializer_class(certifications, many=True)
            response = ResponseClass(result=True, has_data=True, message='Liste des certifications', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()