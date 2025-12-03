from typing import cast
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from myapi.models import Campagne, Cooperative, Culture
from .cooperative_controller import CooperativeController, MonitoringCooperativeController

class ImportationController:
    message = ''
    def __init__(self, file, campagne, sheet_number) -> None:
        self.data_frame = pd.read_excel(file, sheet_name=int(sheet_number))
        # self.data_frame = pd.read_csv(file, delimiter=";", encoding='utf-8')
        self.coops = self.data_frame['COOPERATIVE'].str.strip().drop_duplicates().values
        self.data_frame.fillna('0', inplace=True)
        self.data_frame['SUPERFICIE PARCELLE'] = self.data_frame['SUPERFICIE PARCELLE'].astype(float)
        self.campagne = Campagne.objects.get(pk=campagne)
    
    def getCoop(self):
        try:
            coops = Cooperative.objects.filter(nomCoop__in =self.coops)
            return coops
        except Cooperative.DoesNotExist:
            last_coop = Cooperative.objects.all().order_by('id').last()
            for coop in self.coops:
                new_coop = Cooperative.objects.create(**{"nomCoop": coop, "projet": last_coop.projet, "respo":last_coop.respo})
                Culture.objects.create(**{"libelle":"Cacao", "cooperative":new_coop})
            return Cooperative.objects.filter(nomCoop__in =self.coops)    
    def importer(self):
        try:
            coops = self.getCoop()
            self.data_frame['COOPERATIVE'] = self.data_frame['COOPERATIVE'].str.upper().str.strip()
            for cooperative in coops:
                if cooperative is not None:
                    data = self.data_frame.loc[self.data_frame['COOPERATIVE']==cooperative.nomCoop]
                    cooperative_controller = CooperativeController(coop=cooperative,camp=self.campagne, data=data)
                    cooperative_controller.insertion_producteur()
            self.message = cooperative_controller.message
            self.stats = {
                "total_producteurs": len(cooperative_controller.producteurs_enregistres) + len(cooperative_controller.producteurs_non_enregistres),
                "producteurs_enregistres": len(cooperative_controller.producteurs_enregistres),
                "producteurs_non_enregistres": len(cooperative_controller.producteurs_non_enregistres),
                "total_parcelles": len(cooperative_controller.parcelles_enregistres) + len(cooperative_controller.parcelles_non_enregistres),
                "parcelles_non_enregistres": len(cooperative_controller.parcelles_non_enregistres),
                "parcelles_enregistres": len(cooperative_controller.parcelles_enregistres),
                "total_planting": len(cooperative_controller.planting_enregistres) + len(cooperative_controller.planting_non_enregistres),
                "planting_non_enregistres": len(cooperative_controller.planting_non_enregistres),
                "planting_enregistres": len(cooperative_controller.planting_enregistres),}
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
            