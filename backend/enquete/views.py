from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from myapi.models import Utilisateur
from enquete.controllers import QuestionController
from foret.naiveclasses import ResponseClass
from enquete.models import Enqueteur, Question, Enquete, Reponse, TypeEnquete, TypeQuestion
from enquete.serializers import QuestionSerializer, EnqueteSerializer, TypeEnqueteSerializer, TypeQuestionSerializer

class EnqueteViewSet(ViewSet):
    
    enquete_serializer_class = EnqueteSerializer
    
    @action(detail=False)
    def get_types_enquete(self, request):
        try:
            serializer = TypeEnqueteSerializer(TypeEnquete.objects.all(), many=True)
            response = ResponseClass(result=True, has_data=True, message="Types d'Enquête", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    
    @action(detail=False)
    def get_enquetes(self, request):
        try:
            tel = request.GET.get('technicien_tel')
            enqueteur = Enqueteur.objects.get(user__tel=tel)
            serializer = self.enquete_serializer_class(enqueteur.enquetes.filter(est_ouverte = True), many=True)
            response = ResponseClass(result=True, has_data=True, message="Enquêtes ouvertes", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()
        
    @action(detail=False, methods=['post'])
    def synchronisation(self, request):
        try:
            user = Utilisateur.objects.get(tel=request.data['technicien_tel'])
            enquete = Enquete.objects.get(identifiant = request.data["reponse_enquete"]['identifiant_enquete'])   
            Reponse.objects.create(enquete = enquete, repondant = user, reponses = request.data["reponse_enquete"]["reponse"])
            response = ResponseClass(result=True, has_data=False, message=f"Reponse enregistrée avec succès")
        except Enquete.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Cette enquête a été fermée ou supprimée")
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
        

        
class QuestionViewSet(ViewSet):
       
    question_serializer_class = QuestionSerializer
    
    @action(detail=False)
    def get_types_question(self, request):
        try:
            serializer = TypeQuestionSerializer(TypeQuestion.objects.all(), many=True)
            response = ResponseClass(result=True, has_data=True, message="Types de question", data=serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    
    @action(detail=False, methods=['POST'])
    def insert_questions(self, request):
        try:
            controller_class = QuestionController(file=request.data['fichier'], identifiant_enquete=request.data['identifiant_enquete'])
            controller_class.multiple_insert()
            response = ResponseClass(result=True, has_data=True, message=f"{controller_class.total} questions importées")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
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
    