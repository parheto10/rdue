from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Campagne, CampagneProjet, CategorieEspece, Certification, Cooperative, Countrie, Culture, \
    DetailPlanting, Espece, EspeceSimulate, GroupeProducteur, ModeAcquisition, Monitoring, MonitoringDetail, \
    ObservationMonitoring, ObservationMortalite, Parcelle, Planting, Producteur, Projet, RecolteProducteur, Region, \
    SaisonRecolte, Section, SimulateCarbon, UserProjet, Utilisateur, RDUE, RisqueRDUE, Age, Theme_Enquete, \
    Produit_Phyto, Engrais, Enquete_Social, Age_enfant, Age_scolarise, Enquete_Exploitation, Detail_Age_Homme , \
    Detail_Age_Femme, Detail_phyto, Detail_Engrais, Acte_Propriete, SectionPoint, Point


@admin.register(Section)
class SectionAdmin(ImportExportModelAdmin):
    list_filter = ["cooperative", ]
    ist_display = ['id', 'libelle']

class ProdResource(resources.ModelResource):
    class Meta:
        model = Producteur
        import_id_fields = ('code',)

class ProducteurAdmin(ImportExportModelAdmin):
    list_display = ["code", "nomComplet", "section", "lieu_habitation"]
    list_filter = ["section__cooperative", "section__libelle",]
    search_fields = ["code", "nomComplet", "contacts", ]
    resource_class = ProdResource


class ParcelleResource(resources.ModelResource):
    class Meta:
        model = Parcelle
        import_id_fields = ('code',)


class RecolteResource(resources.ModelResource):
    class Meta:
        model = RecolteProducteur
        import_id_fields = ('code',)

class RecolteResource(resources.ModelResource):
    class Meta:
        model = RecolteProducteur
        import_id_fields = ('code',)

class RecolteProducteurAdmin(ImportExportModelAdmin):
    list_display = ["code", "parcelle", "campagne", "estimation_production", "poids_total"]
    list_filter = ["parcelle__producteur__section__cooperative"]
    search_fields = ["code", "parcelle",]
    resource_class = RecolteResource


@admin.action(description="Set Parcelle Risque")
def set_risque(modeladmin, request, queryset):
    queryset.update(risque="3")

@admin.action(description="Set Parcelle Risque Zéro COOPA-HS")
def set_risque_coopahs(modeladmin, request, queryset):
    queryset.update(risque="5")

@admin.action(description="Set Parcelle is Mappés")
def set_is_mapper(modeladmin, request, queryset):
    queryset.update(is_mapped=True)

@admin.action(description="Set Parcelle is Not Mappés")
def set_is_not_mapper(modeladmin, request, queryset):
    queryset.update(is_mapped=False)

class ParcelleAdmin(ImportExportModelAdmin):
    list_display = ["code", "producteur", "acquisition", "latitude", "longitude", "superficie", "is_mapped"]
    list_filter = ["producteur__section__cooperative", "risque", "is_mapped"]
    search_fields = ["code", "producteur__nomComplet", "latitude", "longitude", "superficie"]
    resource_class = ParcelleResource
    actions = [
        set_risque,
        set_is_mapper,
        set_is_not_mapper
    ]









# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Countrie,ImportExportModelAdmin)
admin.site.register(Projet,ImportExportModelAdmin)
admin.site.register(UserProjet,ImportExportModelAdmin)
admin.site.register(Campagne,ImportExportModelAdmin)
admin.site.register(Espece,ImportExportModelAdmin)
admin.site.register(CategorieEspece,ImportExportModelAdmin)

admin.site.register(SimulateCarbon)
admin.site.register(EspeceSimulate)

admin.site.register(CampagneProjet)

admin.site.register(Region,ImportExportModelAdmin)
admin.site.register(Cooperative,ImportExportModelAdmin)
 

# admin.site.register(Section,ImportExportModelAdmin)
admin.site.register(GroupeProducteur,ImportExportModelAdmin)

admin.site.register(Producteur,ProducteurAdmin)

admin.site.register(Culture,ImportExportModelAdmin)
admin.site.register(ModeAcquisition,ImportExportModelAdmin)
admin.site.register(Parcelle, ParcelleAdmin)

admin.site.register(Planting,ImportExportModelAdmin)
admin.site.register(DetailPlanting,ImportExportModelAdmin)

admin.site.register(Monitoring,ImportExportModelAdmin)
admin.site.register(MonitoringDetail,ImportExportModelAdmin)

admin.site.register(ObservationMonitoring,ImportExportModelAdmin)
admin.site.register(ObservationMortalite,ImportExportModelAdmin)

admin.site.register(SaisonRecolte,ImportExportModelAdmin)
admin.site.register(RecolteProducteur, RecolteProducteurAdmin)
admin.site.register(Certification,ImportExportModelAdmin)


admin.site.register(RDUE)
admin.site.register(RisqueRDUE)


admin.site.register(Age)
admin.site.register(Theme_Enquete)
admin.site.register(Produit_Phyto)
admin.site.register(Engrais)

admin.site.register(Enquete_Social)
admin.site.register(Age_enfant)
admin.site.register(Age_scolarise)
admin.site.register(Enquete_Exploitation)
admin.site.register(Detail_Age_Homme)
admin.site.register(Detail_Age_Femme)
admin.site.register(Detail_phyto)
admin.site.register(Detail_Engrais)
admin.site.register(Acte_Propriete)

admin.site.register(SectionPoint)
admin.site.register(Point)







