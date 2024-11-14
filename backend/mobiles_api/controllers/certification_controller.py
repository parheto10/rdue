from mobiles_api.models import Certificat
from myapi.models import Certification, Parcelle


class CertificationController:
    def synchronisation(self, data, parcelle:Parcelle):
        try:
            code = data['code']
            certification = None if data['certification']==None else Certification.objects.get(pk=data['certification'])
            annee = data['annee']
            certificat, created = Certificat.objects.get_or_create(certification=certification, code=code)
            certificat.annee = annee
            certificat.certification = certification
            certificat.parcelle = parcelle
            certificat.save()
            return certificat
        except Exception as e:
            raise Exception(str(e))