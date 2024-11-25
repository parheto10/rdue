# Externals imports
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# internals imports
from foret.naiveclasses import ResponseClass
from mobiles_api.serializers import CertificationSerializer, CertificatSerializer
from myapi.models import Certification, Parcelle
from mobiles_api.models import Certificat

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
        
class CertificatViewSet(ViewSet):
    serializer_class = CertificatSerializer
    
    @action(detail=False)
    def get_all_certificat(self, request):
        try:
            certificats = Certificat.objects.all()
            serializer = self.serializer_class(certificats, many=True)
            response = ResponseClass(result=True, has_data=True, message='Liste des certificats', data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    
    @action(detail=False, methods=['post'])
    def synchronisation(self, request):
        try:
            code = request.data['code']
            certification = None if request.data['certification']==None else Certification.objects.get(pk=request.data['certification'])
            annee = request.data['annee']
            parcelle = None if request.data['parcelle']==None else Parcelle.objects.get(pk=request.data['parcelle'])
            certificat, created = Certificat.objects.get_or_create(certification=certification, code=code)
            certificat.annee = annee
            certificat.certification = certification
            certificat.parcelle = parcelle
            certificat.save()
            response = ResponseClass(result=True, has_data=False, message='')
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        