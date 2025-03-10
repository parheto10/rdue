"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# views classes imports
from mobiles_api.views import UtilisateurViewSet, CooperativeViewSet, SectionViewSet, CampagneViewSet, ProducteurViewSet, ParcelleViewSet, PlantingViewSet, DetailPlantingViewSet, CertificationViewSet, CertificatViewSet, CultureViewSet, ModeAcquisitionViewSet, EspeceViewSet, ActeProprieteViewSet, ObservationMortaliteViewSet, ObservationMonitoringViewSet, MonitoringViewSet, DetailMonitoringViewSet, CompensationPSEViewSet, CategorieActiviteRetributionViewSet, ActiviteRetributionViewSet, InfoPSEViewSet
from api_importation.views import DataImportation
from enquete.views import EnqueteViewSet, QuestionViewSet
# rest_framework imports
from rest_framework import routers
# Routes de l'api pour les applications mobiles
router = routers.SimpleRouter()
importation = routers.SimpleRouter()

router.register('utilisateur', UtilisateurViewSet, basename='utilisateur')
router.register('cooperative', CooperativeViewSet, basename='cooperative')
router.register('section', SectionViewSet, basename='section')
router.register('campagne', CampagneViewSet, basename='campagne')
router.register('producteur', ProducteurViewSet, basename='producteur')
router.register('parcelle', ParcelleViewSet, basename='parcelle')
router.register('planting', PlantingViewSet, basename='planting')
router.register('detail_planting', DetailPlantingViewSet, basename='detail_planting')
router.register('certification', CertificationViewSet, basename='certification')
router.register('certificat', CertificatViewSet, basename='certificat')
router.register('culture', CultureViewSet, basename='culture')
router.register('mode_acquisition', ModeAcquisitionViewSet, basename='mode_acquisition')
router.register('espece', EspeceViewSet, basename='espece')
router.register('acte_propriete', ActeProprieteViewSet, basename='acte_propriete')
router.register('observation_mortalite', ObservationMortaliteViewSet, basename='observation_mortalite')
router.register('observation_monitoring', ObservationMonitoringViewSet, basename='observation_monitoring')
router.register('monitoring', MonitoringViewSet, basename='monitoring')
router.register('detail_monitoring', DetailMonitoringViewSet, basename='detail_monitoring')
# PSE
router.register('compensation-pse', CompensationPSEViewSet, basename='compensation-pse')
router.register('categorie-activite-retribution', CategorieActiviteRetributionViewSet, basename='categorie-activite-retribution')
router.register('activite-retribution', ActiviteRetributionViewSet, basename='activite-retribution')
router.register('info-pse', InfoPSEViewSet, basename='info-pse')
# Importation Data
importation.register('importation', DataImportation, basename='importation')
# Enquête
router.register('enquete', EnqueteViewSet, basename='enquete')
router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('myapi.urls')),
    path('api-mobile/', include(router.urls)),
    path('api-importation/', include(importation.urls)),
    path('api-auth/',include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
