from decimal import Decimal
from datetime import date
import uuid
from pandas import DataFrame, Series
from myapi.models import Cooperative, Planting, Section, Producteur, Campagne, Parcelle, DetailPlanting, Espece, Culture


class CooperativeController:
    producteurs_non_enregistres = []
    parcelles_non_enregistres = []
    planting_non_enregistres = []
    message = ''
    def __init__(self, coop:Cooperative, camp:Campagne, data:DataFrame) -> None:
        self.especes = ["BANGBAYÉ","ACACIA","ALBIZIA","EMIEN","AKO","BAZA","KAPOTIER","CEDRELA","FROMAGÉ","ORANGER","TIAMA","SIPO","PETIT COLA","GMELINA","SIBO/BAHIA","NIANGON","KPLÉ","ACAJOU / PETITE FEUILLE","ACAJOU / GRAND FEUILLE","ACAJOU","BÉTÉ","POIVRE LONG","IROKO","KOTO","AVOCAT","ASAMELA","DAMEBA","AKODIAKÉDÉ","ILOMBA","APKI","POÉ","TECK","FRAMIRÉ","FRAKÉ","MAKORÉ","BITEI"]
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
        self.data.loc[:,'SECTION'] = self.data['SECTION'].astype(str).str.strip().str.upper()
        self.data.loc[:,'CODE PRODUCTEUR'] = self.data['CODE PRODUCTEUR'].astype(str).str.strip()
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
                    