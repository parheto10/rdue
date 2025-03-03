from decimal import Decimal
from datetime import datetime
import uuid
from pandas import DataFrame, Series
from myapi.models import Cooperative, Monitoring, MonitoringDetail, ObservationMonitoring, ObservationMortalite, Planting, Section, Producteur, Campagne, Parcelle, DetailPlanting, Espece, Culture


class CooperativeController:
    producteurs_non_enregistres = []
    parcelles_non_enregistres = []
    planting_non_enregistres = []
    message = ''
    def __init__(self, coop:Cooperative, camp:Campagne, data:DataFrame) -> None:
        self.especes = ["BANGBAYÉ", "AIELÉ", "ACACIA","ALBIZIA","EMIEN","AKO","BAZA","KAPOTIER","CEDRELA","FROMAGER","ORANGER","TIAMA","SIPO","PETIT COLA","GMELINA","SIBO/BAHIA","NIANGON","KPLÉ","ACAJOU / PETITE FEUILLE","ACAJOU / GRAND FEUILLE","ACAJOU","BÉTÉ","POIVRE LONG","IROKO","KOTO","AVOCAT","ASAMELA","DAMEBA","AKODIAKÉDÉ","ILOMBA","AKPI","POÉ","TECK","FRAMIRÉ","FRAKÉ","MAKORÉ","BITEI"]
        self.cooperative = coop
        self.data = data
        self.campagne = camp
        self.sections = self.data[:]['SECTION'].astype(str).str.strip().str.upper().drop_duplicates().values
        self.insertion_section()
        
    def add_if_not_exist(list:list, item):
        if list.__contains__() is not True:
                list.append(item)

    def code_prod(self, string:str):
        new_string = ''
        index = 0
        for i in range(len(string)):
            i+=1
            if string[-i] == 'P':
                index = i
                break
        new_string = string[0:-index]
        return new_string
    
    def getEspece(self):
        try:
            especes = Espece.objects.filter(libelle__in=self.especes)
            return especes
        except:
            return None
        
    def insertion_prod(self, prod:Series, section:Section):
        try:
            producteur, is_created = Producteur.objects.get_or_create(code=str(prod.get('CODE PRODUCTEUR')))
            if is_created == False:
                self.producteurs_non_enregistres.append(producteur.code)
            else:
                producteur.section = section
                producteur.nomComplet = str(prod.get('NOM DU PRODUCTEUR'))
                producteur.contacts = str(prod.get('NUMERO DE TELEPHONE DU PRODUCTEUR'))
                producteur.lieu_habitation = str(prod.get('LOCALITE'))
                producteur.campagne = self.campagne
                producteur.save()
            return producteur
        except Exception as e:
            self.message = str(e)
        
    def insertion_parcelle(self, prod:Series, producteur:Producteur):
        try:
            code =  prod.get('CODE PARCELLE')
            parcelle, is_created = Parcelle.objects.get_or_create(code=code, producteur = producteur)
            if is_created == False:
                self.parcelles_non_enregistres.append(parcelle.code)
            else:
                parcelle.latitude = str(prod.get('LAT'))
                parcelle.longitude = str(prod.get('LON'))
                parcelle.superficie = float(prod.get('SUPERFICIE PARCELLE'))
                parcelle.culture = Culture.objects.get(cooperative=self.cooperative)
                parcelle.save()
            return parcelle
        except Exception as e:
            self.message = str(e)
        
    def insertion_planting(self, prod:Series, parcelle:Parcelle):
        try:
            date_planting =  prod.get('DATE DE PLANTING')
            code =  f"PLG-{uuid.uuid4().hex.upper()[0:10]}"
            campagne = self.campagne
            planting, is_created = Planting.objects.get_or_create(code = code ,parcelle=parcelle, campagne=campagne)
            if is_created ==  False:
                self.planting_non_enregistres.append(planting.code)
            else:
                planting.date = date_planting # date.fromisoformat(date_planting)
                planting.plant_recus = int(prod.get('NOMBRE DE PLANTS RECUS'))
                planting.plant_existant = int(prod.get('ARBRES EXISTANTS'))
                planting.save()
            return planting
        except Exception as e:
            self.message = str(e)
        
    def insertion_details_planting(self, prod:Series, planting:Planting, espece:Espece):
        try:
            nbre_plants = prod.get(espece.libelle)
            if nbre_plants is not None and int(nbre_plants)>0:
                code = f'DPL-{uuid.uuid4().hex.upper()[0:10]}'
                detail_planting, is_created  = DetailPlanting.objects.get_or_create(code = code, planting=planting)
                detail_planting.espece = espece
                detail_planting.plants = int(prod[espece.libelle])
                detail_planting.save()
                return detail_planting
        except Exception as e:
            self.message = str(e)
                
    def insertion_section(self):
        for section in self.sections:        
            Section.objects.get_or_create(libelle=str(section).strip(), cooperative=self.cooperative)
            
    def insertion_producteur(self):
        nbre_prods = 0
        nbre_parcelles = 0
        nbre_plantings = 0
        nbre_details_planting = 0
        # self.data.loc[:,'SECTION'] = self.data['SECTION'].astype(str).str.strip().str.upper()
        # self.data.loc[:,'CODE PRODUCTEUR'] = self.data['CODE PRODUCTEUR'].astype(str).str.strip()
        try:
            bd_sections = Section.objects.filter(cooperative=self.cooperative)
            nbre_sections = bd_sections.count()
            for section in bd_sections:
                producteurs = self.data.loc[self.data['SECTION']==section.libelle]
                for index, prod in producteurs.iterrows():
                    producteur = self.insertion_prod(prod, section)
                    if producteur is not None:
                        nbre_prods += 1 
                        parcelle = self.insertion_parcelle(prod=prod, producteur=producteur)
                        if parcelle is not None:
                            producteur.nbParc += 1
                            producteur.save()
                            nbre_parcelles += 1 
                            planting = self.insertion_planting(prod=prod, parcelle=parcelle)
                            if planting is not None:
                                nbre_plantings += 1
                                especes = self.getEspece()
                                if especes is not None:
                                    for espece in especes:
                                        detail_planting = self.insertion_details_planting(prod=prod, planting=planting, espece=espece)
                                        if detail_planting is not None:
                                            nbre_details_planting += 1
            self.message = f'Sections: {nbre_sections}\n Producteurs: {nbre_prods}\n Parcelles: {nbre_parcelles}\n Plantings: {nbre_plantings}\n Détails planting: {nbre_details_planting}'
            self.message = self.message + f" Prods: {self.producteurs_non_enregistres} Parcelles: {self.parcelles_non_enregistres}"                          
        except Exception as e:
            self.message = str(e)

class MonitoringCooperativeController:
    def __init__(self, coop:Cooperative, camp:Campagne, data:DataFrame) -> None:
        self.especes = ["BANGBAYÉ","ACACIA","ALBIZIA","EMIEN","AKO","BAZA","KAPOTIER","CEDRELA","FROMAGÉ","ORANGER","TIAMA","SIPO","PETIT COLA","GMELINA","SIBO/BAHIA","NIANGON","KPLÉ","ACAJOU / PETITE FEUILLE","ACAJOU / GRAND FEUILLE","ACAJOU","BÉTÉ","POIVRE LONG","IROKO","KOTO","AVOCAT","ASAMELA","DAMEBA","AKODIAKÉDÉ","ILOMBA","AKPI","POÉ","TECK","FRAMIRÉ","FRAKÉ","MAKORÉ","BITEI"]
        self.cooperative = coop
        self.data = data
        self.campagne = camp
        self.nbre_monitoring = 0
        self.nbre_detail_monitoring = 0
        self.message = ''
        self.list_code_parcelle = []
        
    def get_parcelle(self, code_parcelle:str):
        try:
            parcelle = Parcelle.objects.get(code = code_parcelle, producteur__section__cooperative = self.cooperative)
            return parcelle
        except Exception as e:
            return None
        
    def get_last_planting(self, code_parcelle:str):
        parcelle = self.get_parcelle(code_parcelle=code_parcelle)
        if parcelle is not None:
            return Planting.objects.filter(parcelle = parcelle, campagne = self.campagne).last()
        else:
            self.list_code_parcelle.append(code_parcelle)
            return None
    
    def get_list_detail_planting(self, code_parcelle:str):
        last_planting = self.get_last_planting(code_parcelle=code_parcelle)
        if last_planting is not None:
            details_planting = list(DetailPlanting.objects.filter(planting = last_planting))
            return details_planting
        else:
            return None
        
    def create_monitoring(self, planting:Planting, row:Series):
        try:
            code = f"MNT-{uuid.uuid4().hex.upper()[0:10]}"
            date  = None if row.get('DATE DE MONITORING') == None else row.get('DATE DE MONITORING')
            taux_reussite = Decimal(row.get('TAUX DE SURVIE')) * 100
            monitoring = Monitoring.objects.create(code=code, planting = planting, campagne = planting.campagne)
            monitoring.taux_reussite = taux_reussite
            monitoring.date = date
            monitoring.save()
            return monitoring
        except Exception as e:
            return None     
        
    def insert_causes_de_mortalite(self, monitoring:Monitoring, row:Series):
        try:
            sont_plusieurs_causes = str(row.get('FACTEURS DES MORTALITES')).find('|')
            if sont_plusieurs_causes < 0:
                cause_de_mortalite = ObservationMortalite.objects.get(libelle = str(row.get('FACTEURS DES MORTALITES')))
                ObservationMonitoring.objects.create(monitoring=monitoring, observation = cause_de_mortalite)
            else:
                causes_de_mortalite = list(ObservationMortalite.objects.filter(libelle__in = str(row.get('FACTEURS DES MORTALITES')).split('|')))
                for cause in causes_de_mortalite:
                    ObservationMonitoring.objects.create(monitoring=monitoring, observation = cause)
        except ObservationMortalite.DoesNotExist:
            raise Exception(f"{row.get('FACTEURS DES MORTALITES')}")
        
    def insert_detail_monitoring(self, detail_planting:DetailPlanting, monitoring:Monitoring, row:Series):
        try:
            if row.get(detail_planting.espece.libelle) is not None:
                code = f'DMN-{uuid.uuid4().hex.upper()[0:10]}'
                plant_denombre = int(row.get(detail_planting.espece.libelle))
                taux_reussite = ((plant_denombre/detail_planting.plants) * 100)
                detailMonitoring = MonitoringDetail.objects.create(code=code)
                detailMonitoring.monitoring = monitoring
                detailMonitoring.espece = detail_planting.espece
                detailMonitoring.plant_denombre = plant_denombre
                detailMonitoring.taux_reussite = taux_reussite
                detailMonitoring.save()
                return detailMonitoring
        except Exception as e:
            return None
        
    def multiple_insert_detail_monitoring(self, details_planting:list[DetailPlanting], monitoring:Monitoring, row:Series):
        nbre_detail = 0
        for detail_planting in details_planting:
           detail_monitoring = self.insert_detail_monitoring(detail_planting=detail_planting, monitoring=monitoring, row=row)
           if detail_monitoring is not None:
               nbre_detail +=1
        return nbre_detail
               
    def insert_monitoring(self, row:Series):
        last_planting = self.get_last_planting(code_parcelle=row.get('CODE PARCELLE'))
        if last_planting is not None:
            details_planting = list(DetailPlanting.objects.filter(planting = last_planting, espece__libelle__in = self.especes))
            if len(details_planting) > 0:
                monitoring = self.create_monitoring(planting=last_planting, row=row)
                if monitoring is not None:
                    self.nbre_monitoring += 1
                    if monitoring.taux_reussite < 100:
                        self.insert_causes_de_mortalite(monitoring=monitoring, row=row)
                    self.nbre_detail_monitoring += self.multiple_insert_detail_monitoring(details_planting=details_planting, monitoring=monitoring, row=row)
            else:
                return None
        else:
            return None
        
    def importer_monitoring(self):
        for index, row in self.data.iterrows():
            self.insert_monitoring(row=row)
        self.message = f"Monitoring:{self.nbre_monitoring}\n Détails monitoring: {self.nbre_detail_monitoring} Code Non trouvés: {self.list_code_parcelle}"