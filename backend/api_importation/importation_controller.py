from typing import cast
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from myapi.models import Campagne, Cooperative
from .cooperative_controller import CooperativeController, MonitoringCooperativeController

class ImportationController:
    message = ''
    def __init__(self, file, campagne) -> None:
        self.data_frame = pd.read_excel(file)
        # self.data_frame = pd.read_csv(file, delimiter=";", encoding='utf-8')
        self.coops = self.data_frame['COOPERATIVE'].str.strip().drop_duplicates().values
        self.campagne = Campagne.objects.get(pk=campagne)
    
    def getCoop(self):
        try:
            coops = Cooperative.objects.filter(nomCoop__in =self.coops)
            return coops
        except ObjectDoesNotExist:
            raise Exception(str(ObjectDoesNotExist))
    
    def importer(self):
        try:
            coops = self.getCoop()
            self.data_frame['COOPERATIVE'] = self.data_frame['COOPERATIVE'].str.strip()
            self.data_frame['SECTION'] = self.data_frame['SECTION'].str.strip()
            self.data_frame['CODE PARCELLE'] = self.data_frame['CODE PARCELLE'].str.upper().str.strip()
            self.data_frame['NOM DU PRODUCTEUR'] = self.data_frame['NOM DU PRODUCTEUR'].str.upper().str.strip()
            for cooperative in coops:
                if cooperative is not None:
                    data = self.data_frame.loc[self.data_frame['COOPERATIVE']==cooperative.nomCoop]
                    cooperative_controller = CooperativeController(coop=cooperative,camp=self.campagne, data=data)
                    cooperative_controller.insertion_producteur()
            self.message = cooperative_controller.message
        except Exception as e:
            self.message = str(e)
            
    def importation_monitoring(self):
        try:
            coops = self.getCoop()
            self.data_frame['COOPERATIVE'] = self.data_frame['COOPERATIVE'].str.strip()
            for cooperative in coops:
                if cooperative is not None:
                    data = self.data_frame.loc[self.data_frame['COOPERATIVE']==cooperative.nomCoop]
                    monitoring_cooperative_controller = MonitoringCooperativeController(coop=cooperative,camp=self.campagne, data=data)
                    monitoring_cooperative_controller.importer_monitoring()
            self.message = monitoring_cooperative_controller.message
        except Exception as e:
            self.message = str(e)
            