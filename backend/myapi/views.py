import os
from django.shortcuts import render

from .models import RDUE
from .serializers import CampagneProjetSerializer, CampagneSerializer, CertificationSerializer, \
    CooperativeSerializer, CountrieSerialiser, CultureSerializer, DetailPlantingSerializer, EspeceSerialiser, \
    EspeceSimulateSerializer, GroupeProducteurSerializer, ModeAcquisitionSerializer, MonitoringDetailSerializer, \
    MonitoringSerializer, ObservationMortaliteSerializer, ParcelleSerializer, PlantingSerializer, ProducteurSerializer, \
    ProjetSerializer, RecolteProducteurSerializer, RegionSerializer, SaisonRecolteSerializer, SectionSerializer, \
    SimulateCarbonSerialiser, UserProjetSerializer, UtilisateurSerializer, RdueSerialiser, AgeSerializer, SectionPointSerializer, \
    PointSerializer
from . import models
import random
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from slugify import slugify
from rest_framework.decorators import api_view
import locale
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.views import APIView
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Count,Max,Sum
from django.db.models.functions import TruncMonth
# Create your views here.
from rest_framework.pagination import PageNumberPagination
import xlwt
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
import pandas as pd 
from django.contrib.staticfiles import finders

# from .models import RDUE, Enquete


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomPaginationCarte(PageNumberPagination):
    page_size = 2000
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

#temps de chez nous
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')



class UserList(generics.ListCreateAPIView):
    queryset = models.Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    

class LoginUsersView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = models.Utilisateur.objects.filter(email=email).first()
        
        if user is None:
            return JsonResponse({'bool': False, 'msg': 'Votre compte est introuvable'})
        
        
        if not check_password(password, user.password): 
            return JsonResponse({'bool': False, 'msg': 'Votre mot de passe incorrect !'})
        
        if check_password(password, user.password):
            login(request, user)
        
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=24),
                'iat': datetime.datetime.utcnow()
            }

            # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            
            #connexion reponsable
            if user.is_responsable : 
                projusers = models.Projet.objects.filter(respo_id = user.id,etat =  True)
                
                if len(projusers) > 0 :
                    
                    response.data = {
                         'token':token,
                         'bool':True,
                         'role':'responsable',
                         'proj':True
                     }

                    return response
                elif len(projusers) == 0 :
                    response.data = {
                         'token':token,
                         'bool':True,
                         'role':'responsable',
                         'proj':False
                     }

                    return response
            
            #connexion Client
            if user.is_client : 
                projusers = models.Projet.objects.filter(respo_id = user.id, etat = True)
                
                if len(projusers) > 0 :
                    
                    response.data = {
                         'token':token,
                         'bool':True,
                         'role':'client',
                         'proj':True
                     }

                    return response
                elif len(projusers) == 0 :
                    response.data = {
                         'token':token,
                         'bool':True,
                         'role':'client',
                         'proj':False
                     }

                    return response
                
            #connexion super admin
            if user.is_adg :
                response.data = {
                         'token':token,
                         'bool':True,
                         'role':'adg',
                     }

                return response
        

class UsersView(generics.ListAPIView):
    serializer_class = UtilisateurSerializer
    
    def get_queryset(self):
        if 'token' in self.request.GET:
            token = self.request.GET['token']
            
            if not token:
                return JsonResponse({'failed':True})

            try:
                #print(f"okokokkkookk")
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                try :
                    utilisateur = models.Utilisateur.objects.filter(id=payload['id'])
                    return utilisateur
                except models.Utilisateur.DoesNotExist :
                   return JsonResponse({'failed':True})  
               
            except jwt.ExpiredSignatureError:
                pass
            

class EspeceList(generics.ListAPIView):
    serializer_class = EspeceSerialiser
    queryset = models.Espece.objects.all()
    
@csrf_exempt
def start_simulate_carbone(request):
    peuplement = request.POST.get('peuplement')
    code = ''.join(str(random.randint(0, 9)) for _ in range(4))
    
    simulate = models.SimulateCarbon()
    simulate.anneePeuplement = int(peuplement)
    simulate.code = code
    simulate.save()
    
    return JsonResponse({'bool':True,'simulateID':simulate.id})


class EspeceSimulateList(APIView):
    serializer_class = EspeceSimulateSerializer
    
    def post(self,request):
        simulateID = request.data['simulateID']
        especeID = request.data['espece']
        quantity = request.data['quantity']
        
        simulate = models.SimulateCarbon.objects.get(id=int(simulateID))
        espece = models.Espece.objects.get(id=int(especeID))
        
        #(int(mt)*float(especeItem.co2_annuel)*int(anneePeuplement))*0.001
        if espece.densite == 0 or espece.co2_annuel == 0 :
            return JsonResponse({'bool':False,'msg':'Densité ou CO2 annuel egale a 0'})
        
        
        if len(models.EspeceSimulate.objects.filter(simulate_id = simulate.id,espece_id = espece.id)) == 0 :  
            especeSimulate = models.EspeceSimulate()
            especeSimulate.espece_id = espece.id
            especeSimulate.quantity = int(quantity)
            especeSimulate.simulate_id = simulate.id
            especeSimulate.carboneStocke = (int(quantity)*float(espece.co2_annuel)*simulate.anneePeuplement)*0.001
            
            
            especeSimulate.save()
            
            queryset = models.EspeceSimulate.objects.filter(simulate_id = simulate.id).order_by('-created_at')
            
            especeTab = []
            
            for query in queryset :
                item = {
                    "id":query.espece.id,
                    "libelle":query.espece.libelle,
                    "quantity":query.quantity
                }
                
                especeTab.append(item)
            
            return JsonResponse({'especeTab':especeTab,'bool':True})
        
        else :
            return JsonResponse({'bool':False,'msg':'Espèce deja choisi !'})
        

@csrf_exempt
def resultat_simulate_carbon(request):
    simulateID = request.POST.get('simulateID')
    peuplement = request.POST.get('peuplement')
    
    
    try:
        simulate = models.SimulateCarbon.objects.get(id=int(simulateID))
        especeSimulates = models.EspeceSimulate.objects.filter(simulate_id = simulate.id).order_by('-created_at')
        
        simulate.anneePeuplement = int(peuplement)
        for espece in especeSimulates :
            if simulate.totalCarbone is not None:
                simulate.totalCarbone = simulate.totalCarbone + espece.carboneStocke
        
        simulate.save()
        
        return JsonResponse({'bool':True})
    except models.SimulateCarbon.DoesNotExist:
        return JsonResponse({'bool':False,'msg':"'Desolé une erreur s'est produite !"})
    
    

class SimulateCarboneList(generics.ListAPIView):
    serializer_class = SimulateCarbonSerialiser
    
    def get_queryset(self):
        if 'sID' in self.request.GET:
            sID = self.request.GET['sID']
            queryset = models.SimulateCarbon.objects.filter(id=int(sID))
        
        
        return queryset
    
class EspecesSimulateCarboneList(generics.ListAPIView):
    serializer_class = EspeceSimulateSerializer
    
    def get_queryset(self):
        if 'sID' in self.request.GET:
            sID = self.request.GET['sID']
            simulate = models.SimulateCarbon.objects.get(id=int(sID))
            queryset = models.EspeceSimulate.objects.filter(simulate_id = simulate.id).order_by('-created_at')
            
        return queryset
    
class CountrieList(generics.ListAPIView):
    serializer_class = CountrieSerialiser
    queryset = models.Countrie.objects.all()

@csrf_exempt
def create_projet_users(request):
    nomProjet = request.POST.get('nomProjet')
    countrieID = request.POST.get('countrieID')
    description = request.POST.get('description')
    dateDebut = request.POST.get('dateDebut')
    dateFin = request.POST.get('dateFin')
    objectif = request.POST.get('objectif')
    plant_aproduit = request.POST.get('plant_aproduit')
    carbon_astock = request.POST.get('carbon_astock')
    emp_engageof_proj = request.POST.get('emp_engageof_proj')
    campagne = request.POST.get('campagne')
    userID = request.POST.get('userID')
    
    projet = models.Projet()
    
    #projet 
    projet.nomProjet = nomProjet.upper()
    projet.countrie_id = countrieID
    projet.description = description
    projet.dateDebut = dateDebut
    projet.dateFin = dateFin
    projet.objectif = objectif
    projet.plant_aproduit = float(plant_aproduit)
    projet.carbon_astock = float(carbon_astock)
    projet.emp_engageof_proj = int(emp_engageof_proj)
    projet.respo_id = userID
    projet.save()
    
    #campagneproj = models.CampagneProjet()
    #campagneproj.campagne_id = campagne
    #campagneproj.projet_id = projet.id
    #campagneproj.save()
    #
    #userprojet = models.UserProjet()
    #userprojet.projet_id = projet.id
    #userprojet.utilisateur_id = int(userID)
    #userprojet.save()
    
    return JsonResponse({'bool':True})

@csrf_exempt
def create_new_projet(request):
    nomProjet = request.POST.get('nomProjet')
    countrieID = request.POST.get('countrieID')
    description = request.POST.get('description')
    dateDebut = request.POST.get('dateDebut')
    dateFin = request.POST.get('dateFin')
    objectif = request.POST.get('objectif')
    
    plant_aproduit = request.POST.get('plant_aproduit')
    carbon_astock = request.POST.get('carbon_astock')
    emp_engageof_proj = request.POST.get('emp_engageof_proj')
    
    dateDebutc = request.POST.get('dateDebutc')
    DateFinc = request.POST.get('DateFinc')
    #anneé des campagnes
    deb = datetime.datetime.strptime(dateDebutc,'%Y-%m-%d').year
    fin = datetime.datetime.strptime(DateFinc,'%Y-%m-%d').year
    
    if deb == fin :
        libelle = fin
    else:
        libelle = f"{deb}-{fin}"
    
    userID = request.POST.get('userID')
    
    #CREATION DE CAMPAGNE, PROJET , USER PROJET ,CAMPAGNE PROJET
    campagne = models.Campagne()
    projet = models.Projet()
    
    #projet 
    projet.nomProjet = nomProjet.upper()
    projet.countrie_id = countrieID
    projet.description = description
    projet.dateDebut = dateDebut
    projet.dateFin = dateFin
    projet.objectif = objectif
    projet.plant_aproduit = float(plant_aproduit)
    projet.carbon_astock = float(carbon_astock)
    projet.emp_engageof_proj = int(emp_engageof_proj)
    projet.respo_id = userID
    projet.save()
    
    #campagne
    duree = (fin - deb) * 12

    campagne.dateDebut = dateDebutc
    campagne.DateFin = DateFinc
    campagne.libelle = libelle
    campagne.duree_campagne = f"{duree} Mois"
    campagne.respo_id = userID
    campagne.save()
    
    #campagneproj = models.CampagneProjet()
    #campagneproj.campagne_id = campagne.id
    #campagneproj.projet_id = projet.id
    #campagneproj.save()
    
    
    #userprojet = models.UserProjet()
    #userprojet.projet_id = projet.id
    #userprojet.utilisateur_id = int(userID)
    #userprojet.save()
    
    return JsonResponse({'bool':True,'msg':f"Le projet {nomProjet.upper()} a été crée avec succès. Campgne {libelle} ouverte et en cours."})

class ProjetUserList(generics.ListAPIView):
    serializer_class = UserProjetSerializer
    
    def get_queryset(self):
        if 'userID' in self.request.GET:
            userID = self.request.GET['userID']
            queryset = models.UserProjet.objects.filter(utilisateur_id = int(userID))
            
        if 'projID' in self.request.GET:
            projID = self.request.GET['projID']
            queryset = models.UserProjet.objects.filter(projet_id = int(projID))
            
        return queryset
    

class ProjetList(generics.ListAPIView):
    serializer_class = ProjetSerializer
    
    def get_queryset(self):
        if 'projID' in self.request.GET :
            projID = self.request.GET['projID']
            queryset = models.Projet.objects.filter(id=int(projID))
            nb_producteurs = models.Producteur.objects.filter(section__cooperative__projet_id=int(projID)).count()
            print('nombre de Pructeurs : %s' % (nb_producteurs))
            nb_parcelles = models.Parcelle.objects.filter(
                producteur__section__cooperative__projet_id=int(projID)).count()
            # print(nb_parcelles)
            
        if 'userID' in self.request.GET :
            userID = self.request.GET['userID']
            queryset = models.Projet.objects.filter(respo_id=int(userID))
        
        return queryset
    
class RegionList(generics.ListCreateAPIView):
    serializer_class = RegionSerializer
    queryset = models.Region.objects.all()
    
class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer
    def get_queryset(self):
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Section.objects.filter(cooperative_id = int(coopID))
            # queryset = models.Section.objects.filter(cooperative_id = coopID)
            # print(queryset)
        return queryset
    
class GroupeProList(generics.ListCreateAPIView):
    serializer_class = GroupeProducteurSerializer
    queryset = models.GroupeProducteur.objects.all()

class CultureList(generics.ListCreateAPIView):
    serializer_class = CultureSerializer
    def get_queryset(self):
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Culture.objects.filter(cooperative_id = int(coopID))
            
        return queryset
    
class ModeAcquisitionList(generics.ListCreateAPIView):
    serializer_class = ModeAcquisitionSerializer
    queryset = models.ModeAcquisition.objects.all()
    
class CertificationList(generics.ListAPIView):
    serializer_class = CertificationSerializer
    queryset = models.Certification.objects.all()
    
    
class CooperativeList(generics.ListAPIView):
    serializer_class = CooperativeSerializer
    
    def get_queryset(self):
        if 'projID' in self.request.GET:
            projID = self.request.GET['projID']
            queryset = models.Cooperative.objects.filter(projet_id = int(projID)).order_by("nomCoop")
            nb_producteurs = models.Producteur.objects.filter(section__cooperative__projet_id = int(projID)).count()
            # print('nombre de Pructeurs : %s' %(nb_producteurs))
            nb_parcelles = models.Parcelle.objects.filter(producteur__section__cooperative__projet_id= int(projID)).count()
            # print('nombre de Parcelles : %s' %(nb_parcelles))
            
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Cooperative.objects.filter(id = int(coopID)).order_by("nomCoop")
            
        if 'userID' in self.request.GET:
            userID = self.request.GET['userID']
            queryset = models.Cooperative.objects.filter(respo_id = int(userID)).order_by("nomCoop")
        
        return queryset
    
class CampagneProjList(generics.ListAPIView):
    serializer_class = CampagneProjetSerializer
    def get_queryset(self):
        if 'projId' in self.request.GET:
            projId = self.request.GET['projId']
            queryset = models.CampagneProjet.objects.filter(projet_id = int(projId))
            
        if 'now' in self.request.GET:
            queryset = models.CampagneProjet.objects.filter(campagne__etat =True)
        
        return queryset
    
@csrf_exempt
def create_new_cooperative(request):
    region = request.POST.get('region')
    respCoop = request.POST.get('respCoop')
    nomCoop = request.POST.get('nomCoop').upper()
    contacts = request.POST.get('contacts')
    projetID = request.POST.get('projetID')
    siege = request.POST.get('siege')
    userID = request.POST.get('userID')
    logo = request.FILES.get('logo')
    
    #if len(models.Cooperative.objects.filter(nomCoop = nomCoop,projet_id = int(projetID))) > 0 :
    #    return JsonResponse({'bool':False,'msg':"Cette coopérative existe deja pour ce projet."})
    
    cooperative = models.Cooperative()
    cooperative.region_id = region
    cooperative.respCoop = respCoop.upper()
    cooperative.nomCoop = nomCoop
    cooperative.contacts = contacts
    cooperative.projet_id = projetID
    cooperative.respo_id = userID
    cooperative.logo = logo
    cooperative.siege = siege
    cooperative.save()
    
    return JsonResponse({'bool':True})

@csrf_exempt
def section_save(request):
    libelle = request.POST.get('libelle').upper()
    cooperativeID = request.POST.get('cooperativeID')
    
    if len(models.Section.objects.filter(libelle = libelle,cooperative_id = int(cooperativeID))) > 0 :
        return JsonResponse({'bool':False,'msg':"Cette section existe deja pour cette coopérative."})
    
    section = models.Section()
    section.libelle = libelle
    section.cooperative_id = cooperativeID
    section.save()
    
    return JsonResponse({'bool':True})

@csrf_exempt
def producteur_coop_save(request):
    nomComplet = request.POST.get('nomComplet').upper()
    sectionID = request.POST.get('section')
    code = request.POST.get('code')
    contacts = request.POST.get('contacts')
    nbParc = request.POST.get('nbParc')
    campagne = request.POST.get('campagne')
    groupe = request.POST.get('groupe')
    representant = request.POST.get('representant').upper()
    lieu_habitation = request.POST.get('lieu_habitation').upper()
    photo = request.FILES.get('photo')
    print(code)
    
    section = models.Section.objects.get(id=int(sectionID))
    
    codex  = f"{section.cooperative.nomCoop[:3]}-{''.join(str(random.randint(0, 9)) for _ in range(4))}"
    
    if len(models.Producteur.objects.filter(code = code)) > 0 :
        return JsonResponse({'bool':False,'msg':"Une erreur est subvenu, Essayé a nouveau ! "})
    
    producteur = models.Producteur()
    
    if code == "":
        producteur.code = codex
    else :
        producteur.code = code
        
    
    producteur.section_id = section.id
    producteur.nomComplet = nomComplet
    producteur.contacts = contacts
    producteur.nbParc = int(nbParc)
    producteur.campagne_id = campagne
    producteur.representant = representant
    producteur.groupe_id = groupe
    producteur.lieu_habitation = lieu_habitation
    producteur.photo = photo
    producteur.save()
    
    return JsonResponse({'bool':True,"code":code})
    

class ProducteurListNotPaginate(generics.ListAPIView):
    serializer_class = ProducteurSerializer
    
    def get_queryset(self):
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Producteur.objects.filter(section__cooperative_id = int(coopID)).order_by('-created_at')
            
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            queryset = models.Producteur.objects.filter(Q(code__icontains = q) | Q(nomComplet__icontains = q))

        return queryset

class ProducteurList(generics.ListAPIView):
    serializer_class = ProducteurSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Producteur.objects.filter(section__cooperative_id = int(coopID)).order_by('nomComplet')[:int(limit)]
            
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Producteur.objects.filter(section__cooperative_id = int(coopID)).order_by('nomComplet')

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Producteur.objects.filter(code = prodCode)
            
        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            prod = models.Producteur.objects.filter(code = code).delete()
            queryset = models.Producteur.objects.filter(section__cooperative_id = int(coop)).order_by('-created_at')
            
        if 'q' and 'co'  in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Producteur.objects.filter(section__cooperative_id = int(coopID)).filter( Q(code__icontains = q) | Q(nomComplet__icontains = q))
            

        return queryset
    


################ Parcelle For Carte #################################
class ParcelleListCarte(generics.ListAPIView):
    serializer_class = ParcelleSerializer
    pagination_class = CustomPaginationCarte

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id=int(coopID))[:int(limit)]

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Parcelle.objects.filter(producteur_id=prodCode)

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Parcelle.objects.filter(code=parcId)

        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id=int(coopID))

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative__respo=int(manager))

        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id=int(coopID)).filter(
                Q(producteur__nomComplet__icontains=q) | Q(code__icontains=q))

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.Parcelle.objects.filter(code=code).delete()
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id=int(coop))

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.Parcelle.objects.filter(producteur__section_id=int(sectionID))

        return queryset


class ParcelleList(generics.ListAPIView):
    serializer_class = ParcelleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID))[:int(limit)]

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Parcelle.objects.filter(producteur_id = prodCode)

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Parcelle.objects.filter(code = parcId)


        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID))

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative__respo = int(manager))

        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(producteur__nomComplet__icontains = q) | Q(code__icontains = q))

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.Parcelle.objects.filter(code = code).delete()
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coop))

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.Parcelle.objects.filter(producteur__section_id = int(sectionID))

        return queryset

class ParcelleList_sup_4ha(generics.ListAPIView):
    serializer_class = ParcelleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(superficie__gte=4)[:int(limit)] # super > 4 ha

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Parcelle.objects.filter(producteur_id = prodCode)

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Parcelle.objects.filter(code = parcId)


        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(superficie__gt=4)

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative__respo = int(manager)).filter(superficie__gt=4)

        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(producteur__nomComplet__icontains = q) | Q(code__icontains = q)).filter(superficie__gt=4)

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.Parcelle.objects.filter(code = code).delete()
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coop)).filter(superficie__gt=4)

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.Parcelle.objects.filter(producteur__section_id = int(sectionID)).filter(superficie__gt=4)

        return queryset

class ParcelleList_inf_4ha(generics.ListAPIView):
    serializer_class = ParcelleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(superficie__lte=4)[:int(limit)] # super > 4 ha

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Parcelle.objects.filter(producteur_id = prodCode).filter(superficie__lte=4)

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Parcelle.objects.filter(code = parcId)


        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(superficie__lte=4)

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative__respo = int(manager)).filter(superficie__lte=4)

        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(producteur__nomComplet__icontains = q) | Q(code__icontains = q)).filter(superficie__lte=4)

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.Parcelle.objects.filter(code = code).delete()
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coop)).filter(superficie__lte=4)

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.Parcelle.objects.filter(producteur__section_id = int(sectionID)).filter(superficie__lte=4)

        return queryset

class ParcelleList_risque_modere(generics.ListAPIView):
    serializer_class = ParcelleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(risque_id=2) | Q(risque_id=1))[:int(limit)] # super > 4 ha

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Parcelle.objects.filter(producteur_id = prodCode).filter(Q(risque_id=2) | Q(risque_id=1))

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Parcelle.objects.filter(code = parcId)

        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(risque_id=2) | Q(risque_id=1))

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative__respo = int(manager)).filter(Q(risque_id=2) | Q(risque_id=1))

        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(producteur__nomComplet__icontains = q) | Q(code__icontains = q)).filter(Q(risque_id=2) | Q(risque_id=1))

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.Parcelle.objects.filter(code = code).delete()
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coop)).filter(Q(risque_id=2) | Q(risque_id=1))

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.Parcelle.objects.filter(producteur__section_id = int(sectionID)).filter(Q(risque_id=2) | Q(risque_id=1))

        return queryset
    

class ParcelleList_plus4_non_mapper(generics.ListAPIView):
    serializer_class = ParcelleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(superficie__gt=4).filter(is_mapped=False)[:int(limit)] # super > 4 ha non mapper
            print(queryset)

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.Parcelle.objects.filter(producteur_id = prodCode).filter(is_mapped=False).filter(superficie__gt=4)

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Parcelle.objects.filter(code = parcId)

        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(is_mapped=False).filter(superficie__gt=4)

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative__respo = int(manager)).filter(is_mapped=False).filter(superficie__gt=4)

        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopID)).filter(Q(producteur__nomComplet__icontains = q) | Q(code__icontains = q)).filter(is_mapped=False).filter(superficie__gt=4)

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.Parcelle.objects.filter(code = code).delete()
            queryset = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coop)).filter(is_mapped=False).filter(superficie__gt=4)

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.Parcelle.objects.filter(producteur__section_id = int(sectionID)).filter(is_mapped=False).filter(superficie__gt=4)

        return queryset
    

class ProductionList(generics.ListAPIView):
    serializer_class = RecolteProducteurSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if 'coopID' and 'page' in self.request.GET:
            coopID = self.request.GET['coopID']
            limit = self.request.GET['page']
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur__section__cooperative_id = int(coopID)).order_by("producteur")[:int(limit)] # super > 4 ha non mapper
            print(queryset)

        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur_id = prodCode)

        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.RecolteProducteur.objects.filter(code = parcId)

        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur__section__cooperative_id = int(coopID))

        if 'manager' in self.request.GET:
            manager = self.request.GET['manager']
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur__section__cooperative__respo = int(manager))
        if 'q' and 'co' in self.request.GET:
            q = self.request.GET['q']
            coopID = self.request.GET['co']
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur__section__cooperative_id = int(coopID)).filter(Q(parcelle__producteur__nomComplet__icontains = q) | Q(code__icontains = q))

        if 'code' and 'coop' in self.request.GET:
            code = self.request.GET['code']
            coop = self.request.GET['coop']
            parcelle = models.RecolteProducteur.objects.filter(code = code).delete()
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur__section__cooperative_id = int(coop))

        if 'sectionID' in self.request.GET:
            sectionID = self.request.GET['sectionID']
            queryset = models.RecolteProducteur.objects.filter(parcelle__producteur__section_id = int(sectionID))

        return queryset





@csrf_exempt
def create_new_parcelle(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    superficie = request.POST.get('superficie')
    certification = request.POST.get('certification')
    annee_certificat = request.POST.get('annee_certificat')
    annee_acquis = request.POST.get('annee_acquis')
    culture = request.POST.get('culture')
    prodCode = request.POST.get('prodCode')
    campagne = request.POST.get('campagne')
    acquisition = request.POST.get('acquisition')
    code_certif = request.POST.get('code_certif')

    try:
        producteur = models.Producteur.objects.get(code=prodCode)
        
        if len(models.Parcelle.objects.filter(producteur_id = producteur.code)) >= producteur.nbParc :
            return JsonResponse({'bool':False,'msg':f"Désolé {producteur.nomComplet} ne dispose que de {producteur.nbParc} parcelle(s)"})
            
        parcelle = models.Parcelle()
        if len(models.Parcelle.objects.filter(producteur_id = producteur.code)) >= 0 :
            tot ='P0'+str(len(models.Parcelle.objects.filter(producteur_id = producteur.code)) + 1)
            parcelle.code = "%s%s" % (producteur.code, tot)
        
        code = parcelle.code
        parcelle.latitude = latitude
        parcelle.longitude = longitude
        parcelle.superficie = float(superficie)
        parcelle.certificat_id = certification
        parcelle.annee_acquis = annee_acquis
        parcelle.annee_certificat = annee_certificat
        parcelle.culture_id = culture
        parcelle.campagne_id = campagne
        parcelle.producteur_id = producteur.code
        parcelle.acquisition_id = acquisition
        parcelle.code_certif = code_certif
        parcelle.save()
        
        return JsonResponse({'bool':True,"code":code})
    except models.Producteur.DoesNotExist:
        return JsonResponse({'bool':False,"msg":"Désolé ce producteur est introuvable"})
    

            
class CampagneList(generics.ListCreateAPIView):
    serializer_class = CampagneSerializer
    
    def get_queryset(self):
        if 'userID' in self.request.GET:
            userId = self.request.GET['userID']
            queryset = models.Campagne.objects.filter(respo = int(userId))
            return queryset
        
        if 'resp' and 'open' in self.request.GET:
            resp = self.request.GET['resp']
            queryset = models.Campagne.objects.filter(respo = int(resp),etat=True)
            return queryset


@csrf_exempt
def create_new_campagne(request):
    dateDebut = request.POST.get('dateDebut')
    DateFin = request.POST.get('DateFin')
    #anneé des campagnes
    deb = datetime.datetime.strptime(dateDebut,'%Y-%m-%d').year
    fin = datetime.datetime.strptime(DateFin,'%Y-%m-%d').year
    
    if deb == fin :
        libelle = fin
    else:
        libelle = f"{deb}-{fin}"
    
    userID = request.POST.get('userID')
    
    if len(models.Campagne.objects.filter(etat=True)) > 0:
        return JsonResponse({'bool':False,"msg":"Une campagne est actuellement ouverte"})
    
    
    campagne = models.Campagne()
    
    duree = (fin - deb) * 12

    campagne.dateDebut = dateDebut
    campagne.DateFin = DateFin
    campagne.libelle = libelle
    campagne.duree_campagne = f"{duree} Mois"
    campagne.respo_id = userID
    campagne.save()
    
    return JsonResponse({'bool':True,'lib':libelle})


@csrf_exempt
def new_planting_save(request):
    especes = request.POST.getlist('especes')
    plants = request.POST.getlist('plants')
    plant_existant = request.POST.get('plant_existant')
    campagne = request.POST.get('campagne')
    date = request.POST.get('date')
    parcID = request.POST.get('parcID')
    note = request.POST.get('note')
    
    tot_espece = 0
    
    parcelle = models.Parcelle.objects.get(code=parcID)
    
    for nb in plants:
        tot_espece = tot_espece + int(nb)
        
    planting = models.Planting()
    
    planting.code = f"PLG-{''.join(str(random.randint(0, 9)) for _ in range(4))}"
    planting.date = date
    planting.parcelle_id = parcelle.code
    planting.plant_recus = tot_espece
    planting.plant_existant = int(plant_existant)
    planting.note_plant_existant = note
    planting.campagne_id = campagne
    planting.save()

    for esp, nb in zip(especes,plants):
        detailPlanting = models.DetailPlanting()
        detailPlanting.code = f"DPL-{''.join(str(random.randint(0, 9)) for _ in range(4))}"
        detailPlanting.espece_id = int(esp)
        detailPlanting.plants = int(nb)
        detailPlanting.planting_id = planting.code
        detailPlanting.save()
        #print(detailPlanting.code)

    return JsonResponse({'bool':True,'parc':parcelle.code})

class PlantingList(generics.ListAPIView):
    serializer_class = PlantingSerializer
    
    def get_queryset(self):
        if 'parcId' in self.request.GET:
            parcId = self.request.GET["parcId"]
            queryset = models.Planting.objects.filter(parcelle_id = parcId)
        
        if 'delete' and 'parc' in self.request.GET:
            delete = self.request.GET["delete"]
            parc = self.request.GET["parc"]
            planting = models.Planting.objects.get(code=delete)
            planting.delete()
            
            queryset = models.Planting.objects.filter(parcelle_id = parc)
            
        return queryset
        
class CauseMortaliteList(generics.ListAPIView):
    serializer_class = ObservationMortaliteSerializer
    queryset = models.ObservationMortalite.objects.all()
    
class DetailPlantingList(generics.ListAPIView):
    serializer_class = DetailPlantingSerializer
    
    def get_queryset(self):
        if 'plantCode' in self.request.GET:
            plantCode = self.request.GET['plantCode']
            queryset = models.DetailPlanting.objects.filter(planting_id=plantCode)
        
        return queryset
    
@csrf_exempt
def create_new_monitoring(request):
    especes = request.POST.getlist('especes')
    observations = request.POST.getlist('observations')
    plants = request.POST.getlist('plants')
    plant_recus = request.POST.getlist('plant_recus')
    campagne = request.POST.get('campagne')
    date = request.POST.get('date')
    plantCode = request.POST.get('planting')
    
    tot_denombre = 0
    planting = models.Planting.objects.get(code=plantCode)
    
    for tot in plants:
        tot_denombre = tot_denombre + int(tot)
        
    monitoring = models.Monitoring()
    monitoring.code = f"MNT-{''.join(str(random.randint(0, 9)) for _ in range(4))}"
    monitoring.planting_id = planting.code
    monitoring.date = date
    monitoring.campagne_id = campagne
    monitoring.taux_reussite = (tot_denombre*100)/planting.plant_recus
    monitoring.save()
    
    if observations != []:
        for cause in observations:
            causeMortalite = models.ObservationMonitoring()
            causeMortalite.monitoring_id = monitoring.code
            causeMortalite.observation_id = int(cause)
            causeMortalite.save()
            
    for esp,pl,rc in zip(especes,plants,plant_recus) :
        especeMonitoring = models.MonitoringDetail()
        especeMonitoring.code = f"MNT-{''.join(str(random.randint(0, 9)) for _ in range(4))}"
        especeMonitoring.monitoring_id = monitoring.code
        especeMonitoring.espece_id = esp
        especeMonitoring.plant_denombre = int(pl)
        especeMonitoring.taux_reussite = (int(pl)*100)/int(rc)
        especeMonitoring.save()
        
    
    
    return JsonResponse({'bool':True})


class MonitoringList(generics.ListAPIView):
    serializer_class = MonitoringSerializer
    
    def get_queryset(self):
        if 'parcId' in self.request.GET:
            parcId = self.request.GET['parcId']
            queryset = models.Monitoring.objects.filter(planting__parcelle__code = parcId)
            
        if 'parc' and 'code' in self.request.GET:
            parc = self.request.GET['parc']
            code = self.request.GET['code']
            monitoring = models.Monitoring.objects.get(code = code)
            monitoring.delete()
            
            queryset = models.Monitoring.objects.filter(planting__parcelle__code = parc)
        return queryset

class DetailMonitoringList(generics.ListAPIView):
    serializer_class = MonitoringDetailSerializer

    def get_queryset(self):
        if 'code' in self.request.GET:
            code = self.request.GET['code']
            queryset = models.MonitoringDetail.objects.filter(monitoring = code)
            
        return queryset
    
class SaisonProductionList(generics.ListAPIView):
    serializer_class = SaisonRecolteSerializer
    def get_queryset(self):
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.SaisonRecolte.objects.filter(cooperative_id = int(coopID))
        
        return queryset
    
class RecolteProductionList(generics.ListAPIView):
    serializer_class = RecolteProducteurSerializer
    def get_queryset(self):
        if 'coopID' in self.request.GET:
            coopID = self.request.GET['coopID']
            queryset = models.RecolteProducteur.objects.filter(producteur__section__cooperative_id = int(coopID))
            
        if 'prodCode' in self.request.GET:
            prodCode = self.request.GET['prodCode']
            queryset = models.RecolteProducteur.objects.filter(producteur_id = prodCode)
        
        return queryset
    
    
@csrf_exempt
def culture_save(request):
    libelle = request.POST.get('libelle').upper()
    prix = request.POST.get('prix_unitaire_culture')
    cooperativeID = request.POST.get('cooperativeID')
    
    if len(models.Culture.objects.filter(cooperative_id = int(cooperativeID), libelle = libelle)) > 0 :
        return JsonResponse({'bool':False,'msg':"Cette Culture existe deja."})
    
    culture = models.Culture()
    culture.libelle = libelle
    culture.prix_unitaire_culture = float(prix)
    culture.cooperative_id = cooperativeID
    culture.save()
    
    return JsonResponse({'bool':True})


@csrf_exempt
def saison_save(request):
    libelle = request.POST.get('libelle').upper()
    cooperativeID = request.POST.get('cooperativeID')
    
    if len(models.SaisonRecolte.objects.filter(cooperative_id = int(cooperativeID),libelle = libelle)) > 0 :
        return JsonResponse({'bool':False,'msg':"Cette saison existe deja."})
    
    saison = models.SaisonRecolte()
    saison.libelle = libelle
    saison.cooperative_id = cooperativeID
    saison.save()
    
    return JsonResponse({'bool':True})


@csrf_exempt
def create_new_recolte(request):
    prodCode = request.POST.get("producteur")
    campagne_id = request.POST.get("campagne")
    saison_id = request.POST.get("saison")
    culture_id = request.POST.get("culture")
    lieu_production = request.POST.get("lieu_production")
    nbre_sacs = request.POST.get("nbre_sacs")
    poids = request.POST.get("poids_total")
    prix_total = request.POST.get("prix_total")
    
    recolte = models.RecolteProducteur()
    recolte.code = f"RPD-{''.join(str(random.randint(0, 9)) for _ in range(4))}"
    recolte.producteur_id = prodCode
    recolte.campagne_id = campagne_id
    recolte.saison_id = saison_id
    recolte.culture_id = culture_id
    recolte.lieu_production = lieu_production
    recolte.nbre_sacs = int(nbre_sacs)
    recolte.poids_total = float(poids)
    recolte.prix_total = float(prix_total)
    recolte.save()
    
    return JsonResponse({'bool':True})


@csrf_exempt
def coop_producteur_update(request):
    nomComplet = request.POST.get('nomComplet').upper()
    sectionID = request.POST.get('section')
    contacts = request.POST.get('contacts')
    nbParc = request.POST.get('nbParc')
    lieu_habitation = request.POST.get('lieu_habitation').upper()
    photo = request.FILES.get('photo')
    prodCode = request.POST.get('producteur')
    
    producteur = models.Producteur.objects.get(code=prodCode)
    producteur.nomComplet = nomComplet
    producteur.section_id = sectionID
    producteur.contacts = contacts
    producteur.nbParc = nbParc
    producteur.lieu_habitation = lieu_habitation
    if photo :
        producteur.photo = photo
        
    producteur.save()
    
    return JsonResponse({'bool':True})

@csrf_exempt
def update_coop_parcelle(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    superficie = request.POST.get('superficie')
    certification = request.POST.get('certification')
    annee_certificat = request.POST.get('annee_certificat')
    annee_acquis = request.POST.get('annee_acquis')
    culture = request.POST.get('culture')
    code = request.POST.get('code')
    acquisition = request.POST.get('acquisition')
    code_certif = request.POST.get('code_certif')
    
    #print(certification,culture,acquisition)
    parcelle = models.Parcelle.objects.get(code=code)
    parcelle.latitude = latitude
    parcelle.longitude = longitude
    parcelle.superficie = float(superficie)
    
    if certification !="undefined":
        parcelle.certificat_id = certification
        
    parcelle.annee_acquis = annee_acquis
    parcelle.annee_certificat = annee_certificat
    
    if  culture !="undefined":
        parcelle.culture_id = culture
        
    if acquisition !="undefined":
        parcelle.acquisition_id = acquisition
    parcelle.code_certif = code_certif
    parcelle.save()
    
    return JsonResponse({'bool':True})




def export_prod_cooperative(request):
    format_exp = request.GET.get('format')
    campagne = request.GET.get('campagne')
    coopId = request.GET.get('coopID')
    cooperative = models.Cooperative.objects.get(id=int(coopId))
    
    if campagne == '':
        producteurs = models.Producteur.objects.filter(section__cooperative_id = int(coopId)).order_by('nomComplet')
    else :
        producteurs = models.Producteur.objects.filter(section__cooperative_id = int(coopId),campagne_id=int(campagne)).order_by('nomComplet')
    
    if format_exp == 'PDF':
        template_path = 'pdf/producteur_pdf.html'
        context = {
            'cooperative':cooperative,
            'producteurs':producteurs,
        }
         
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Producteurs.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        #print(html)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')
        
        return response 
    
    elif format_exp == 'EXCEL':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Producteurs')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['CODE', 'NOM ET PRENOMS', 'SECTION', 'NBRE DE PARCELLE', 'CONTACT', 'LOCALITE']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = producteurs.values_list(
            'code',
            'nomComplet',
            'section__libelle',
            'nbParc',
            'contacts',
            'lieu_habitation'
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    

def export_parcelle_cooperative(request):
    format_exp = request.GET.get('format')
    campagne = request.GET.get('campagne')
    coopId = request.GET.get('coopID')
    cooperative = models.Cooperative.objects.get(id=int(coopId))

    if campagne == '':
        parcelles = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopId)).order_by('producteur__nomComplet')
    else :
        parcelles = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopId),campagne_id=int(campagne)).order_by('producteur__nomComplet')

    
        
    if format_exp == 'PDF' :
        template_path = 'pdf/parcelles_pdf.html'
        context = {
            'cooperative':cooperative,
            'parcelles':parcelles,
        }
         
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Parcelles.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        #print(html)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')
        
        return response 
    
    elif format_exp == 'EXCEL':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="parcelles.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Parcelle')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['CODE', 'NOM ET PRENOMS', 'SECTION', 'CULTURE', 'CERTIFICATION', 'SUPERFICIE', 'LATITUDE', 'LONGITUDE']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = parcelles.values_list(
            'code',
            'producteur__nomComplet',
            'producteur__section__libelle',
            'culture__libelle',
            'certificat__libelle',
            'superficie',
            'latitude',
            'longitude'
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

def export_parcelle4plus_non_mapped(request):
    format_exp = request.GET.get('format')
    campagne = request.GET.get('campagne')
    coopId = request.GET.get('coopID')
    cooperative = models.Cooperative.objects.get(id=int(coopId))

    if campagne == '':
        parcelles = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopId)).filter(superficie__gt=4).filter(is_mapped=False).order_by('producteur__nomComplet')
    else :
        parcelles = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopId),campagne_id=int(campagne)).filter(is_mapped=False).order_by('producteur__nomComplet')

    if format_exp == 'PDF' :
        template_path = 'pdf/parcelles_pdf.html'
        context = {
            'cooperative':cooperative,
            'parcelles':parcelles,
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Parcelles.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        #print(html)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')

        return response

    elif format_exp == 'EXCEL':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="parcelles.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Parcelle')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['CODE', 'NOM ET PRENOMS', 'SECTION', 'CERTIFICATION', 'LATITUDE', 'LONGITUDE', 'SUPERFICIE']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = parcelles.values_list(
            'code',
            'producteur__nomComplet',
            'producteur__section__libelle',
            'certificat__libelle',
            'latitude',
            'longitude',
            'superficie',
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

def export_parcelle_a_risque(request):
    format_exp = request.GET.get('format')
    campagne = request.GET.get('campagne')
    coopId = request.GET.get('coopID')
    cooperative = models.Cooperative.objects.get(id=int(coopId))

    if campagne == '':
        parcelles = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopId)).filter(Q(risque_id=2) | Q(risque_id=1)).order_by('producteur__nomComplet')
    else :
        parcelles = models.Parcelle.objects.filter(producteur__section__cooperative_id = int(coopId),campagne_id=int(campagne)).filter(Q(risque_id=2) | Q(risque_id=1)).order_by('producteur__nomComplet')

    if format_exp == 'PDF' :
        template_path = 'pdf/parcelles_a_risque_pdf.html'
        context = {
            'cooperative':cooperative,
            'parcelles':parcelles,
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Parcelles_a_risque.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        #print(html)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')

        return response

    elif format_exp == 'EXCEL':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="parcelles.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Parcelle')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['CODE', 'NOM ET PRENOMS', 'SECTION', 'CERTIFICATION', 'LATITUDE', 'LONGITUDE', 'SUPERFICIE', 'RISQUE']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = parcelles.values_list(
            'code',
            'producteur__nomComplet',
            'producteur__section__libelle',
            'certificat__libelle',
            'latitude',
            'longitude',
            'superficie',
            'risque__libelle',
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    
    
@csrf_exempt
def saison_update(request):
    libelle = request.POST.get('libelle')
    id = request.POST.get('id')
    
    saison = models.SaisonRecolte.objects.get(id=int(id))
    saison.libelle = libelle
    saison.save()
    
    return JsonResponse({'bool':True})

@csrf_exempt
def section_update(request):
    libelle = request.POST.get('libelle')
    id = request.POST.get('id')
    
    section = models.Section.objects.get(id=int(id))
    section.libelle = libelle
    section.save()
    
    return JsonResponse({'bool':True})

@csrf_exempt
def culture_update(request):
    libelle = request.POST.get('libelle')
    id = request.POST.get('id')
    prix_unitaire_culture = request.POST.get('prix_unitaire_culture')
    
    culture = models.Culture.objects.get(id=int(id))
    culture.libelle =  libelle
    culture.prix_unitaire_culture = float(prix_unitaire_culture)
    
    culture.save()
    
    return JsonResponse({'bool':True})


@csrf_exempt
def cooperative_update(request):
    region = request.POST.get('region')
    respCoop = request.POST.get('respCoop')
    nomCoop = request.POST.get('nomCoop')
    contacts = request.POST.get('contacts')
    projetID = request.POST.get('projetID')
    id = request.POST.get('id')
    siege = request.POST.get('siege')
    #print(projetID)
    cooperative =models.Cooperative.objects.get(id=int(id))
    cooperative.region_id = region
    cooperative.respCoop = respCoop
    cooperative.nomCoop = nomCoop
    cooperative.contacts = contacts
    if projetID != "undefined" :
        cooperative.projet_id = projetID
        
    cooperative.siege = siege
    
    cooperative.save()
    
    return JsonResponse({'bool':True})
def producteur_by_section_state(request):
    cooperativeID = request.GET['cooperative']
    data = []
    sectionCoop = models.Section.objects.filter(cooperative_id = int(cooperativeID)).annotate(producteur_num=Count('producteur'))
    
    for sect in sectionCoop :
        listeData = {
            "libelle":sect.libelle,
            "prod_num":sect.producteur_num
        }
        data.append(listeData)
    
    return JsonResponse({'bool':True,'dataSection':data})

def parcelle_by_section_state(request):
    cooperativeID = request.GET['cooperative']
    data = []
    # sectionCoop = models.Section.objects.filter(cooperative_id = int(cooperativeID)).annotate(producteur_num=Count('producteur'))
    sectionCoop = models.Section.objects.filter(cooperative_id = int(cooperativeID)).annotate(producteur_num=Count('producteur'))

    for sect in sectionCoop :
        listeData = {
            "libelle":sect.libelle,
            "prod_num":sect.producteur_num
        }
        data.append(listeData)
    return JsonResponse({'bool':True,'dataSection':data})

#Parcelle Par Risque
def parcelle_by_risque_state(request):
    cooperativeID = request.GET['cooperative']
    data = []
    # sectionCoop = models.Section.objects.filter(cooperative_id = int(cooperativeID)).annotate(producteur_num=Count('producteur'))
    riqueCoop = models.RisqueRDUE.objects.filter(cooperative_id = int(cooperativeID)).annotate(parcelle_num=Count('parcelle')).order_by("-id")
    # print(riqueCoop)

    for risque in riqueCoop :
        listeData = {
            "libelle":risque.libelle,
            "parcelle_num":risque.parcelle_num
        }
        data.append(listeData)
    return JsonResponse({'bool':True,'dataRisque':data})




@csrf_exempt
def analyse_rdue(request):
    entite = request.POST.get('entite')
    produits = request.POST.get('produits')
    chaine_appro = request.POST.get('chaine_appro')
    pays_origine = request.POST.get('pays_origine')
    fournisseur = request.POST.get('fournisseur')
    zone_arisque = request.POST.get('zone_arisque')
    liste_zone = request.POST.get('liste_zone')
    exp_illegale = request.POST.get('exp_illegale')
    mesure_preventives = request.POST.get('mesure_preventives')
    suivi_mesure = request.POST.get('suivi_mesure')
    efficacite_mesure = request.POST.get('efficacite_mesure')
    communication = request.POST.get('communication')
    action_comm = request.POST.get('action_comm')
    action_non_conformite = request.POST.get('action_non_conformite')

    analyse = RDUE.objects.create(
        entite =  entite,
        produits = produits,
        chaine_appro = chaine_appro,
        pays_origine = pays_origine,
        fournisseur = fournisseur,
        zone_arisque = zone_arisque,
        liste_zone = liste_zone,
        exp_illegale =  exp_illegale,
        mesure_preventives = mesure_preventives,
        suivi_mesure = suivi_mesure,
        efficacite_mesure = efficacite_mesure,
        communication = communication,
        action_comm = action_comm,
        action_non_conformite = action_non_conformite,
    )

    if analyse :
        return JsonResponse({'bool': True, 'msg': 'Enregistrement Effectué avec Succès'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Ooops... Reessayé svp !'})


class ListeAnalyse(generics.ListAPIView):
    queryset = RDUE.objects.all()
    serializer_class = RdueSerialiser

class AgeList(generics.ListCreateAPIView):
    serializer_class = AgeSerializer
    queryset = models.Age.objects.all()



class SectionPointListe(generics.ListAPIView):
    serializer_class = SectionPointSerializer
    queryset = models.SectionPoint.objects.all()


class PointList(generics.ListAPIView):
    serializer_class = PointSerializer
    queryset = models.Point.objects.all()


# def create_enquete(request):
#     producteur =request.POST.get('producteur')
#     nb_epouse = request.POST.get('nb_epouse')
#     enfant_mineur = request.POST.get('enfant_mineur')
#     enfant_majeur = request.POST.get('enfant_majeur')
#     nb_enfant = request.POST.get('nb_enfant')
#     enfant_scolarise = request.POST.get('enfant_scolarise')
#     nb_personne = request.POST.get('nb_personne')
#     is_manoeuvre = request.POST.get('manoeuvre')
#     is_manoeuvre_femme = request.POST.get('manoeuvre_femme')
#     nb_manoeuvre_femme = request.POST.get('nb_manoeuvre_femme')
#     type_manoeuvre = request.POST.get('type_manoeuvre')
#     nb_manoeuvre = request.POST.get('nb_manoeuvre')
#     is_ouvrier_mineur= request.POST.get('is_ouvrier_mineur')
#     nb_ouvrier_mineur = request.POST.get('nb_ouvrier_mineur')
#     salaire_ouvrier = request.POST.get('salaire_ouvrier')
#     utilisation_produit_phyto = request.POST.get('utilisation_produit_phyto')
#     is_eau_potable = request.POST.get('is_eau_potable')
#     is_electricite = request.POST.get('is_electricite')
#     is_soins = request.POST.get('is_soins')
#     nb_dispensaire = request.POST.get('nb_dispensaire')
#     dtce_dispensaire = request.POST.get('dtce_dispensaire')
#     nb_ecole_primaire = request.POST.get('nb_ecole_primaire')
#     dtce_ecole_primaire = request.POST.get('dtce_ecole_primaire')
#     is_college = request.POST.get('is_college')
#     nb_college = request.POST.get('nb_college')
#     dtce_college = request.POST.get('dtce_college')
#     is_banque = request.POST.get('is_banque')
#     nb_banque = request.POST.get('nb_banque')
#     dtce_banque = request.POST.get('dtce_banque')
#
#     enquete = Enquete.objects.create(
#         producteur = producteur,
#         nb_epouse = nb_epouse,
#         enfant_mineur = enfant_mineur,
#         enfant_majeur = enfant_majeur,
#         nb_enfant = nb_enfant,
#         enfant_scolarise = enfant_scolarise,
#         nb_personne  = nb_personne,
#         is_manoeuvre = is_manoeuvre,
#         is_manoeuvre_femme = is_manoeuvre_femme,
#         nb_manoeuvre_femme = nb_manoeuvre_femme,
#         type_manoeuvre = type_manoeuvre,
#         nb_manoeuvre = nb_manoeuvre,
#         is_ouvrier_mineur = is_ouvrier_mineur,
#         nb_ouvrier_mineur = nb_ouvrier_mineur,
#         salaire_ouvrier = salaire_ouvrier,
#         utilisation_produit_phyto = utilisation_produit_phyto,
#         is_eau_potable = is_eau_potable,
#         is_electricite = is_electricite,
#         is_soins = is_soins,
#         nb_dispensaire = nb_dispensaire,
#         dtce_dispensaire = dtce_dispensaire,
#         nb_ecole_primaire = nb_ecole_primaire,
#         dtce_ecole_primaire = dtce_ecole_primaire,
#         is_college = is_college,
#         nb_college = nb_college,
#         dtce_college = dtce_college,
#         is_banque = is_banque,
#         nb_banque = nb_banque,
#         dtce_banque = dtce_banque,
#     )
#
#     if enquete :
#         return JsonResponse({'bool': True, 'msg': 'Enregistrement Effectué avec Succès'})
#     else:
#         return JsonResponse({'bool': False, 'msg': 'Ooops... Reessayé svp !'})



# class EnqueteList(generics.ListCreateAPIView):
#     serializer_class = EnqueteSerializer
#     queryset = models.Enquete.objects.all()

    
    
    

    