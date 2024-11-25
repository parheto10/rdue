from django.urls import path,include
from . import views

urlpatterns = [
    path('users/',views.UserList.as_view()),
    path('login/',views.LoginUsersView.as_view()),
    path('users-clients/',views.UsersView.as_view()),
    path('especes/',views.EspeceList.as_view()),
    path('countries-list/',views.CountrieList.as_view()),
    
    path('start-simulate/',views.start_simulate_carbone),
    path('espece-simulate/',views.EspeceSimulateList.as_view()),
    path('resultat-simulate/',views.resultat_simulate_carbon),
    path('simulate-list/',views.SimulateCarboneList.as_view()),
    path('especes-simulate-list/',views.EspecesSimulateCarboneList.as_view()),
    
    path('create-new-proj/',views.create_new_projet),
    path('proj-users-list/',views.ProjetUserList.as_view()),
    path('proj-list/',views.ProjetList.as_view()),
    
    
    path('region-list/',views.RegionList.as_view()),
    path('section-list/',views.SectionList.as_view()),
    path('groupe-prod-list/',views.GroupeProList.as_view()),
    path('mode-acquisition-list/',views.ModeAcquisitionList.as_view()),
    path('culture-list/',views.CultureList.as_view()),
    
    path('create-new-cooperative/',views.create_new_cooperative),
    path('cooperative-list/',views.CooperativeList.as_view()),
    path('campagne-proj-list/',views.CampagneProjList.as_view()),
    
    path('producteur-coop-save/',views.producteur_coop_save),
    path('section-save/',views.section_save),
    path('producteurs-list-paginate/',views.ProducteurList.as_view()),
    path('producteurs-list/',views.ProducteurListNotPaginate.as_view()),
    path('parcelles-list/',views.ParcelleList.as_view()),
    path('productions-list/',views.ProductionList.as_view()),
    

    path('parcelles-list-sup-4ha/',views.ParcelleList_sup_4ha.as_view()), #parcelles-list-sup-4ha
    path('parcelles-list-inf-4ha/',views.ParcelleList_inf_4ha.as_view()), #parcelles-list-inf-4ha
    path('parcelles-list-modere/',views.ParcelleList_risque_modere.as_view()), #parcelles-list-modere
    path('parcelles-list-sup-4ha-non-mapper/',views.ParcelleList_plus4_non_mapper.as_view()), #parcelles-list-4ha-non-mapper

    

    path('parcelles-carte/',views.ParcelleListCarte.as_view()), ##### Parcelles For Carte
    path('create-new-parcelle/',views.create_new_parcelle),
    
    path('campagnes-list/',views.CampagneList.as_view()),
    path('create-new-campagne/',views.create_new_campagne),
    
    path('new-planting-save/',views.new_planting_save),
    path('planting-list/',views.PlantingList.as_view()),
    
    path('obervation-list/',views.CauseMortaliteList.as_view()),
    path('detail-planting-list/',views.DetailPlantingList.as_view()),
    path('create-new-monitoring/',views.create_new_monitoring),
    
    path('monitoring-list/',views.MonitoringList.as_view()),
    path('detail-monitoring-list/',views.DetailMonitoringList.as_view()),
    
    path('saison-recoltes-list/',views.SaisonProductionList.as_view()),
    path('recoltes-producteurs-list/',views.RecolteProductionList.as_view()),
    
    path('culture-save/',views.culture_save),
    path('saison-save/',views.saison_save),
    
    path('create-new-recolte/',views.create_new_recolte),
    path('coop-producteur-update/',views.coop_producteur_update),
    path('update-coop-parcelle/',views.update_coop_parcelle),
    
    path('export-prod-cooperative/',views.export_prod_cooperative),
    path('export-parcelle-cooperative/',views.export_parcelle_cooperative),
    path('export-parcelle-cooperative-non-mapper/',views.export_parcelle4plus_non_mapped),
    path('export-parcelle-cooperative-a-risque/',views.export_parcelle_a_risque),

    
    
    path('certification-list/',views.CertificationList.as_view()),
    
    path('saison-update/',views.saison_update),
    path('section-update/',views.section_update),
    path('culture-update/',views.culture_update),
    
    path('cooperative-update/',views.cooperative_update),
    path('create-projet-users/',views.create_projet_users),
    
    path('producteurs-by-section/', views.producteur_by_section_state),
    path('parcelle_by_risque/', views.parcelle_by_risque_state),


    ############## ANALYSE RDUE #####################
    path('analyses_rdue/',views.ListeAnalyse.as_view()),
    path('create_analyse/',views.analyse_rdue),

    ############## ENQUETES #####################
    path('ages_liste/',views.AgeList.as_view()),
    # path('create_enquete/',views.create_enquete),

    ############## POINTS #####################
    path('section_point/',views.SectionPointListe.as_view()),
    path('points/',views.PointList.as_view()),
]