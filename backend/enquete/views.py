from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from myapi.models import Utilisateur
from enquete.controllers import ConditionController, QuestionController, EnqueteController
from foret.naiveclasses import ResponseClass
from enquete.models import Enqueteur, Question, Enquete, Reponse, TypeEnquete, TypeQuestion
from enquete.serializers import ConditionSerializer, QuestionSerializer, EnqueteSerializer, ReponseSerializer, TypeEnqueteSerializer, TypeQuestionSerializer
import pandas as pd

class EnqueteViewSet(ViewSet):
    
    enquete_serializer_class = EnqueteSerializer
    enquete_controller = EnqueteController()

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            enquete_serializer = self.enquete_serializer_class(self.enquete_controller.insert(data=request.data), many=False)
            response = ResponseClass(result=True, has_data=True, message="Enquete créée avec succès", data=enquete_serializer.data)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()
    
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
    def all(self, request):
        try:
            user = Utilisateur.objects.get(pk=request.GET.get('user_id'))
            serializer = self.enquete_serializer_class(Enquete.objects.filter(created_by=user), many=True)
            response = ResponseClass(result=True, has_data=True, message="Toutes les enquêtes", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
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
            data_frame = pd.read_excel(request.data['fichier'])
            enquete = Enquete.objects.get(identifiant = request.data['identifiant_enquete'])
            controller_class = QuestionController(data_frame=data_frame, enquete=enquete)
            condition_controller_class = ConditionController(data_frame=data_frame, enquete=enquete)
            controller_class.multiple_insert()
            condition_controller_class.multiple_insert()
            response = ResponseClass(result=True, has_data=True, message=f"{controller_class.total} questions importées et {condition_controller_class.total} conditions importées")
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
        
    @action(detail=False)
    def questions(self, request):
        try:
            identifiant = self.request.GET.get('enquete_identifiant')
            questions = Question.objects.all() if identifiant is None  else  Question.objects.filter(enquete__identifiant = identifiant) 
            serializer = self.question_serializer_class( questions, many=True)
            response = ResponseClass(result=True, has_data=True, message="Questions de l'enquête {identifiant}", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()

    @action(detail=False, methods=['DELETE'], url_path='delete')
    def delete_question(self, request):
        try:
            id_question = self.request.GET.get('id_question')
            questions = Question.objects.filter(id=id_question)
            questions.delete()
            response = ResponseClass(result=True, has_data=True, message="Question supprimée")
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()

    @action(detail=False, methods=['PUT'], url_path='update')
    def update_question(self, request):
        try:
            question = Question.objects.get(pk=request.data['id'])
            nbre = QuestionController.update(question=question, data=request.data)
            if nbre > 0:
                response = ResponseClass(result=True, has_data=True, message="Question mise à jour")
            else:
                response = ResponseClass(result=False, has_data=False, message="Erreur de validation")
        except Question.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Question non trouvée")
        finally:
            return response.json_response()
        
    @action(detail=False)
    def get_conditions_question(self, request):
        try:
            tel = self.request.GET.get('technicien_tel')
            enqueteur = Enqueteur.objects.get(user__tel=tel)
            questions =  Question.objects.filter(enquete__in = enqueteur.enquetes.filter(est_ouverte = True)) 
            conditions = []
            for question in questions:
                conditions += question.conditions.all()
            serializer = ConditionSerializer(conditions, many=True)
            response = ResponseClass(result=True, has_data=True, message="Conditions d'enquêtes ouvertes", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        finally:
            return response.json_response()


class ReponseViewSet(ViewSet):
    reponse_serializer_class = ReponseSerializer

    @action(detail=False)
    def all(self, request):
        try:
            identifiant = self.request.GET.get('enquete_identifiant')
            questions = Reponse.objects.all() if identifiant is None  else  Reponse.objects.filter(enquete__identifiant = identifiant) 
            serializer = self.reponse_serializer_class( questions, many=True)
            response = ResponseClass(result=True, has_data=True, message="Reponses d'enquête", data=serializer.data)
        except Enqueteur.DoesNotExist:
            response = ResponseClass(result=False, has_data=False, message="Ce technicien n'existe pas dans la base")
        finally:
            return response.json_response()
      