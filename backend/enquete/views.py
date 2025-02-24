from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from foret.naiveclasses import ResponseClass
from enquete.models import Enqueteur, Question, Enquete
from enquete.serializers import QuestionSerializer, EnqueteSerializer

class EnqueteViewSet(ViewSet):
    
    enquete_serializer_class = EnqueteSerializer
    question_serializer_class = QuestionSerializer
    
    @action(detail=False)
    def get_enquetes(self, request):
        try:
            tel = self.request.GET.get('technicien_tel')
            enqueteur = Enqueteur.objects.get(user__tel=tel)
            serializer = self.enquete_serializer_class(enqueteur.enquetes.filter(est_ouverte = True), many=True)
            response = ResponseClass(result=True, has_data=True, message="Enquêtes ouvertes", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()
        
    @action(detail=False)
    def get_questions(self, request):
        try:
            tel = self.request.GET.get('technicien_tel')
            enqueteur = Enqueteur.objects.get(user__tel=tel)
            questions =  Question.objects.filter(enquete__in = enqueteur.enquetes.filter(est_ouverte = True)) 
            serializer = self.question_serializer_class( questions, many=True)
            response = ResponseClass(result=True, has_data=True, message="Questions d'enquêtes ouvertes", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()
       
        
    