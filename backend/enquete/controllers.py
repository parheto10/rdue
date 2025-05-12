import pandas as pd

from enquete.models import Enquete, Question, TypeQuestion

class QuestionController:
    total = 0
    
    def __init__(self, file, identifiant_enquete) -> None:
        self.data_frame = pd.read_excel(file)
        self.enquete = Enquete.objects.get(identifiant = identifiant_enquete)
    
    
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
    
    def multiple_insert(self):
        for _, row in self.data_frame.iterrows():
            self.insert(row=row)