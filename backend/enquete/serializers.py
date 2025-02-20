from rest_framework.serializers import ModelSerializer

from enquete.models import Question, TypeEnquete, Enquete, TypeQuestion, Reponse

class TypeEnqueteSerializer(ModelSerializer):
    class Meta:
        model = TypeEnquete
        fields = '__all__'
        
class EnqueteSerializer(ModelSerializer):
    type_enquete = TypeEnqueteSerializer(many = False)
    class Meta:
        model = Enquete
        fields = '__all__'
        
class TypeQuestionSerializer(ModelSerializer):
    class Meta:
        model = TypeQuestion
        fields = '__all__'
        
class QuestionSerializer(ModelSerializer):
    type_question = TypeQuestionSerializer(many = False)
    class Meta:
        model = Question
        fields = '__all__'

class ReponseSerializer(ModelSerializer):
    class Meta:
        model = Reponse
        fields = '__all__'
        