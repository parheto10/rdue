from rest_framework import viewsets
from .models import (
    InformationCooperative, CategorieEthnique, StatutMatrimonial, InfoProducteur, StatutMenage,
    Conjoint, Enfant, TypeScolarite, Scolarite, EnfantScolarite, TypeTachesChampetre,
    TacheChampetre, InfoParcelle, DocumentationFonciere, EnfantHasTacheChampetre,
    IndicateurRisqueTacheChampetre, EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetre,
    TypeActionMesureAttenuationTacheChampetre, MesureAttenuationTacheChampetre, Favorabilite,
    AvantageCultureEspece, Abattage, DetailAbattage, TypeMesureAttenuationAgroforesterie,
    MesureAttenuationAgroforesterie, DetailMesureAttenuationAgroforesterieAbattage,
    DetailMesureAttenuationAgroforesteriePlanting, CategorieProduit, TypeProduit, Produit,
    ProduitHasProducteur, ParcelleHasProduit, TypeActionMesureAttenuationPhyto,
    MesureAttenuationPhyto, Organigramme, PlanningAnnuel, ActionMenee, RapportAuditInterne
)
from .serializers import (
    InformationCooperativeSerializer, CategorieEthniqueSerializer, StatutMatrimonialSerializer, InfoProducteurSerializer, StatutMenageSerializer,
    ConjointSerializer, EnfantSerializer, TypeScolariteSerializer, ScolariteSerializer, EnfantScolariteSerializer, TypeTachesChampetreSerializer,
    TacheChampetreSerializer, InfoParcelleSerializer, DocumentationFonciereSerializer, EnfantHasTacheChampetreSerializer,
    IndicateurRisqueTacheChampetreSerializer, EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetreSerializer,
    TypeActionMesureAttenuationTacheChampetreSerializer, MesureAttenuationTacheChampetreSerializer, FavorabiliteSerializer,
    AvantageCultureEspeceSerializer, AbattageSerializer, DetailAbattageSerializer, TypeMesureAttenuationAgroforesterieSerializer,
    MesureAttenuationAgroforesterieSerializer, DetailMesureAttenuationAgroforesterieAbattageSerializer,
    DetailMesureAttenuationAgroforesteriePlantingSerializer, CategorieProduitSerializer, TypeProduitSerializer, ProduitSerializer,
    ProduitHasProducteurSerializer, ParcelleHasProduitSerializer, TypeActionMesureAttenuationPhytoSerializer,
    MesureAttenuationPhytoSerializer, OrganigrammeSerializer, PlanningAnnuelSerializer, ActionMeneeSerializer, RapportAuditInterneSerializer
)

class InformationCooperativeViewSet(viewsets.ModelViewSet):
    queryset = InformationCooperative.objects.all()
    serializer_class = InformationCooperativeSerializer

class CategorieEthniqueViewSet(viewsets.ModelViewSet):
    queryset = CategorieEthnique.objects.all()
    serializer_class = CategorieEthniqueSerializer

class StatutMatrimonialViewSet(viewsets.ModelViewSet):
    queryset = StatutMatrimonial.objects.all()
    serializer_class = StatutMatrimonialSerializer

class InfoProducteurViewSet(viewsets.ModelViewSet):
    queryset = InfoProducteur.objects.all()
    serializer_class = InfoProducteurSerializer

class StatutMenageViewSet(viewsets.ModelViewSet):
    queryset = StatutMenage.objects.all()
    serializer_class = StatutMenageSerializer

class ConjointViewSet(viewsets.ModelViewSet):
    queryset = Conjoint.objects.all()
    serializer_class = ConjointSerializer

class EnfantViewSet(viewsets.ModelViewSet):
    queryset = Enfant.objects.all()
    serializer_class = EnfantSerializer

class TypeScolariteViewSet(viewsets.ModelViewSet):
    queryset = TypeScolarite.objects.all()
    serializer_class = TypeScolariteSerializer

class ScolariteViewSet(viewsets.ModelViewSet):
    queryset = Scolarite.objects.all()
    serializer_class = ScolariteSerializer

class EnfantScolariteViewSet(viewsets.ModelViewSet):
    queryset = EnfantScolarite.objects.all()
    serializer_class = EnfantScolariteSerializer

class TypeTachesChampetreViewSet(viewsets.ModelViewSet):
    queryset = TypeTachesChampetre.objects.all()
    serializer_class = TypeTachesChampetreSerializer

class TacheChampetreViewSet(viewsets.ModelViewSet):
    queryset = TacheChampetre.objects.all()
    serializer_class = TacheChampetreSerializer

class InfoParcelleViewSet(viewsets.ModelViewSet):
    queryset = InfoParcelle.objects.all()
    serializer_class = InfoParcelleSerializer

class DocumentationFonciereViewSet(viewsets.ModelViewSet):
    queryset = DocumentationFonciere.objects.all()
    serializer_class = DocumentationFonciereSerializer

class EnfantHasTacheChampetreViewSet(viewsets.ModelViewSet):
    queryset = EnfantHasTacheChampetre.objects.all()
    serializer_class = EnfantHasTacheChampetreSerializer

class IndicateurRisqueTacheChampetreViewSet(viewsets.ModelViewSet):
    queryset = IndicateurRisqueTacheChampetre.objects.all()
    serializer_class = IndicateurRisqueTacheChampetreSerializer

class EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetreViewSet(viewsets.ModelViewSet):
    queryset = EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetre.objects.all()
    serializer_class = EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetreSerializer

class TypeActionMesureAttenuationTacheChampetreViewSet(viewsets.ModelViewSet):
    queryset = TypeActionMesureAttenuationTacheChampetre.objects.all()
    serializer_class = TypeActionMesureAttenuationTacheChampetreSerializer

class MesureAttenuationTacheChampetreViewSet(viewsets.ModelViewSet):
    queryset = MesureAttenuationTacheChampetre.objects.all()
    serializer_class = MesureAttenuationTacheChampetreSerializer

class FavorabiliteViewSet(viewsets.ModelViewSet):
    queryset = Favorabilite.objects.all()
    serializer_class = FavorabiliteSerializer

class AvantageCultureEspeceViewSet(viewsets.ModelViewSet):
    queryset = AvantageCultureEspece.objects.all()
    serializer_class = AvantageCultureEspeceSerializer

class AbattageViewSet(viewsets.ModelViewSet):
    queryset = Abattage.objects.all()
    serializer_class = AbattageSerializer

class DetailAbattageViewSet(viewsets.ModelViewSet):
    queryset = DetailAbattage.objects.all()
    serializer_class = DetailAbattageSerializer

class TypeMesureAttenuationAgroforesterieViewSet(viewsets.ModelViewSet):
    queryset = TypeMesureAttenuationAgroforesterie.objects.all()
    serializer_class = TypeMesureAttenuationAgroforesterieSerializer

class MesureAttenuationAgroforesterieViewSet(viewsets.ModelViewSet):
    queryset = MesureAttenuationAgroforesterie.objects.all()
    serializer_class = MesureAttenuationAgroforesterieSerializer

class DetailMesureAttenuationAgroforesterieAbattageViewSet(viewsets.ModelViewSet):
    queryset = DetailMesureAttenuationAgroforesterieAbattage.objects.all()
    serializer_class = DetailMesureAttenuationAgroforesterieAbattageSerializer

class DetailMesureAttenuationAgroforesteriePlantingViewSet(viewsets.ModelViewSet):
    queryset = DetailMesureAttenuationAgroforesteriePlanting.objects.all()
    serializer_class = DetailMesureAttenuationAgroforesteriePlantingSerializer

class CategorieProduitViewSet(viewsets.ModelViewSet):
    queryset = CategorieProduit.objects.all()
    serializer_class = CategorieProduitSerializer

class TypeProduitViewSet(viewsets.ModelViewSet):
    queryset = TypeProduit.objects.all()
    serializer_class = TypeProduitSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitHasProducteurViewSet(viewsets.ModelViewSet):
    queryset = ProduitHasProducteur.objects.all()
    serializer_class = ProduitHasProducteurSerializer

class ParcelleHasProduitViewSet(viewsets.ModelViewSet):
    queryset = ParcelleHasProduit.objects.all()
    serializer_class = ParcelleHasProduitSerializer

class TypeActionMesureAttenuationPhytoViewSet(viewsets.ModelViewSet):
    queryset = TypeActionMesureAttenuationPhyto.objects.all()
    serializer_class = TypeActionMesureAttenuationPhytoSerializer

class MesureAttenuationPhytoViewSet(viewsets.ModelViewSet):
    queryset = MesureAttenuationPhyto.objects.all()
    serializer_class = MesureAttenuationPhytoSerializer

class OrganigrammeViewSet(viewsets.ModelViewSet):
    queryset = Organigramme.objects.all()
    serializer_class = OrganigrammeSerializer

class PlanningAnnuelViewSet(viewsets.ModelViewSet):
    queryset = PlanningAnnuel.objects.all()
    serializer_class = PlanningAnnuelSerializer

class ActionMeneeViewSet(viewsets.ModelViewSet):
    queryset = ActionMenee.objects.all()
    serializer_class = ActionMeneeSerializer

class RapportAuditInterneViewSet(viewsets.ModelViewSet):
    queryset = RapportAuditInterne.objects.all()
    serializer_class = RapportAuditInterneSerializer