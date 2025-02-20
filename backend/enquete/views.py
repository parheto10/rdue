from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from foret.naiveclasses import ResponseClass
from enquete.models import Enqueteur, Question
from enquete.serializers import QuestionSerializer

class EnqueteViewSet(ViewSet):
    
    serializer_class = QuestionSerializer
    
    @action(detail=False)
    def get_enquetes(self, request):
        try:
            tel = self.request.GET.get('technicien_tel')
            enqueteur = Enqueteur.objects.get(user__tel=tel)
            questions =  Question.objects.filter(enquete__in = enqueteur.enquetes.filter(est_ouverte = True)) 
            serializer = self.serializer_class( questions, many=True)
            response = ResponseClass(result=True, has_data=True, message=f'Enquêtes ouvertes', data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()
       
        
    