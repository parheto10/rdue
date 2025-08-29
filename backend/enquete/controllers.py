import uuid
import pandas as pd

from myapi.models import Campagne, Projet, Utilisateur
from enquete.models import Condition, Enquete, Question, TypeEnquete, TypeQuestion

class QuestionController:
    total = 0
    
    def __init__(self, data_frame:pd.DataFrame, enquete:Enquete) -> None:
        self.data_frame = data_frame
        self.enquete = enquete

    def split_string(self, row:pd.Series):
        if row.get('CHOIX') is not None:
            if str(row.get('CHOIX')).find(";"):
                return str(row.get('CHOIX')).split(';')
            else:
                return str(row.get('CHOIX')).split(':')
        else:
            None
    
    def insert(self, row:pd.Series):
        value = {}
        try:
            value['type_question'] = TypeQuestion.objects.get(libelle = row.get('TYPE'))
            value['enquete'] = self.enquete
            value['est_obligatoire'] = True if str(row.get('EST_OBLIGATOIRE')).upper() == 'OUI' else False
            value['libelle'] = row.get('LIBELLE')
            value['choix'] = self.split_string(row=row)
            question = Question.objects.create(**value)
            self.total += 1
            return question
        except Exception as e:
            raise Exception(str(e))
        
    def update(self, question:Question, data:dict):
        value = {}
        try:
            question.type_question = TypeQuestion.objects.get(libelle = data.get('type_question'))
            question.enquete =  Enquete.objects.get(libelle = data.get('enquete'))
            question.est_obligatoire = str(data.get('est_obligatoire')).capitalize()
            question.libelle = data.get('libelle')
            # question.choix = data.get('choix')
            question.save()
            return question
        except Exception as e:
            raise Exception(str(e))
    
    def multiple_insert(self):
        for _, row in self.data_frame.iterrows():
            self.insert(row=row)

class EnqueteController:
    def insert(self, data:dict):
        try:
            data['identifiant'] =  f"E{uuid.uuid4().hex.upper()[0:10]}Q"
            data['campagne'] = Campagne.objects.get(id=int(data.get('campagne')))
            data['type_enquete'] = TypeEnquete.objects.get(id=int(data.get('type_enquete')))
            data['est_ouverte'] = str(data.get('est_ouverte')).capitalize()
            data['projet'] = Projet.objects.get(id=int(data.get('projet')))
            data['created_by'] = Utilisateur.objects.get(id=int(data.get('created_by')))
            enquete = Enquete.objects.create(**data)
            return enquete
        except Exception as e:
            raise Exception(str(e))


class ConditionController:
    total = 0

    def __init__(self, data_frame:pd.DataFrame, enquete:Enquete) -> None:
        self.data_frame = data_frame
        self.enquete = enquete
        self.questions = Question.objects.filter(enquete = self.enquete)
        self.lignes_conditionnelles = self.data_frame[self.data_frame['CONDITION'] != '']
        self.lignes_sous_condition = self.data_frame[self.data_frame['SOUS_CONDITION'] != '']

    def insert(self, question_principale:Question, question_cible:Question, valeur:str):
        try:
            condition = Condition.objects.create(question_principale=question_principale, question_cible=question_cible, valeur=valeur)
            self.total += 1
            return condition
        except Exception as e:
            raise Exception(str(e))
        
    def multiple_insert(self):
        for _, row in self.lignes_conditionnelles.iterrows():
            question_principale = self.questions.get(libelle=row.get('LIBELLE'))
            lignes_sous_condition = self.lignes_sous_condition[self.lignes_sous_condition['SOUS_CONDITION'] == row.get('CONDITION')]
            for _, row_sous_condition in lignes_sous_condition.iterrows():
                question_cible = self.questions.get(libelle=row_sous_condition.get('LIBELLE'))
                valeur = row_sous_condition.get('VALEUR')
                self.insert(question_principale=question_principale, question_cible=question_cible, valeur=valeur)
        