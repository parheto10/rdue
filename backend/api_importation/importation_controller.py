from typing import cast
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from myapi.models import Campagne, Cooperative
from .cooperative_controller import CooperativeController

class ImportationController:
    message = ''
    def __init__(self, file, campagne) -> None:
        self.data_frame = pd.read_csv(file, delimiter=";", encoding='utf-8')
        self.coops = self.data_frame['COOPERATIVE'].drop_duplicates().values
        self.campagne = Campagne.objects.get(pk=campagne)
    
    def getCoop(self):
        try:
            coops = Cooperative.objects.filter(nomCoop__in = self.coops)
            return coops
        except ObjectDoesNotExist:
            return None
    
    def importer(self):
        try:
            coops = self.getCoop()
            for cooperative in coops:
                if cooperative is not None:
                    data = self.data_frame.loc[self.data_frame['COOPERATIVE']==cooperative.nomCoop]
                    cooperative_controller = CooperativeController(coop=cooperative,camp=self.campagne, data=data)
                    cooperative_controller.insertion_producteur()
            self.message = cooperative_controller.message
        except Exception as e:
            self.message = str(e)
            