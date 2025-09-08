from rest_framework import serializers
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

class InformationCooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationCooperative
        fields = '__all__'

class CategorieEthniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieEthnique
        fields = '__all__'

class StatutMatrimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutMatrimonial
        fields = '__all__'

class InfoProducteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoProducteur
        fields = '__all__'

class StatutMenageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutMenage
        fields = '__all__'

class ConjointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjoint
        fields = '__all__'

class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfant
        fields = '__all__'

class TypeScolariteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeScolarite
        fields = '__all__'

class ScolariteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scolarite
        fields = '__all__'

class EnfantScolariteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnfantScolarite
        fields = '__all__'

class TypeTachesChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTachesChampetre
        fields = '__all__'

class TacheChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacheChampetre
        fields = '__all__'

class InfoParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoParcelle
        fields = '__all__'

class DocumentationFonciereSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentationFonciere
        fields = '__all__'

class EnfantHasTacheChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnfantHasTacheChampetre
        fields = '__all__'

class IndicateurRisqueTacheChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicateurRisqueTacheChampetre
        fields = '__all__'

class EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnfantHasTacheChampetreHasIndicateurRisqueTacheChampetre
        fields = '__all__'

class TypeActionMesureAttenuationTacheChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeActionMesureAttenuationTacheChampetre
        fields = '__all__'

class MesureAttenuationTacheChampetreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesureAttenuationTacheChampetre
        fields = '__all__'

class FavorabiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorabilite
        fields = '__all__'

class AvantageCultureEspeceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvantageCultureEspece
        fields = '__all__'

class AbattageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abattage
        fields = '__all__'

class DetailAbattageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailAbattage
        fields = '__all__'

class TypeMesureAttenuationAgroforesterieSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMesureAttenuationAgroforesterie
        fields = '__all__'

class MesureAttenuationAgroforesterieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesureAttenuationAgroforesterie
        fields = '__all__'

class DetailMesureAttenuationAgroforesterieAbattageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailMesureAttenuationAgroforesterieAbattage
        fields = '__all__'

class DetailMesureAttenuationAgroforesteriePlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailMesureAttenuationAgroforesteriePlanting
        fields = '__all__'

class CategorieProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieProduit
        fields = '__all__'

class TypeProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduit
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class ProduitHasProducteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitHasProducteur
        fields = '__all__'

class ParcelleHasProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelleHasProduit
        fields = '__all__'

class TypeActionMesureAttenuationPhytoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeActionMesureAttenuationPhyto
        fields = '__all__'

class MesureAttenuationPhytoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesureAttenuationPhyto
        fields = '__all__'

class OrganigrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organigramme
        fields = '__all__'

class PlanningAnnuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningAnnuel
        fields = '__all__'

class ActionMeneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionMenee
        fields = '__all__'

class RapportAuditInterneSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapportAuditInterne
        fields = '__all__'