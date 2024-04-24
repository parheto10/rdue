from typing import cast
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from myapi.models import Cooperative
from .cooperative_controller import CooperativeController

class ImportationController:
    message = ''
    def __init__(self, file) -> None:
        self.data_frame = pd.read_csv(file, delimiter=";", encoding='utf-8')
        self.coops = self.data_frame['COOPERATIVE'].drop_duplicates().values
    
    def getCoop(self):
        try:
            coops = Cooperative.objects.filter(nomCoop__in = self.coops)
            return coops
        except ObjectDoesNotExist:
            return None
    
    def importer(self):
        try:
            cmpt = 0
            coops = self.getCoop()
            for cooperative in coops:
                if cooperative is not None:
                    data = self.data_frame.loc[self.data_frame['COOPERATIVE']==cooperative.nomCoop]
                    cooperative_controller = CooperativeController(coop=cooperative, data=data)
                    result = cooperative_controller.insertion_producteur()
                    if result:
                        cmpt += 1
            return cmpt
        except Exception as e:
            self.message = str(e)
            