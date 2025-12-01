from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from foret.naiveclasses import ResponseClass
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import pandas as pd

class GeoportailViewSet(ViewSet):
    raster_path = str(settings.GEODATA_ROOT) + '/ocs2020.tif'
    polygone_file = str(settings.GEODATA_ROOT) + '/polygon.geojson'
    value_to_class = {
    1: 'Forêt dense',
    2: 'Forêt claire',
    3: 'Forêt galerie',
    4: 'Forêt secondaire/forêt dégradée',
    5: 'Mangrove',
    6: 'Plantation forestière/Reboisement',
    7: 'Forêt marécageuse/Forêt sur sol hydromorphe',
    8: 'Plantation de Café',
    9: 'Plantation de Cacao',
    10: 'Plantation d’Hévéa',
    11: 'Plantation de Palmier à huile',
    12: 'Plantation de Coco',
    13: 'Plantation d’Anacarde',
    14: 'Plantation fruitière / Arboricultures',
    15: 'Aménagement agricole/Autres cultures/Vergers/Jachères',
    16: 'Savane arborée',
    17: 'Formations arbustives/ Fourrés',
    18: 'Formations herbacées',
    19: 'Plan d’eau, Cours et voies d’eau',
    20: 'Zone marécageuse',
    21: 'Habitat humain, Infrastructures',
    22: 'Affleurement rocheux',
    23: 'Sol nu'
    }

    # Palette de couleurs réalistes pour chaque classe
    value_to_color = {
    1: "#00441b",
    2: "#006d2c",
    3: "#238b45",
    4: "#41ae76",
    5: "#78c679",
    6: "#a1d99b",
    7: "#c7e9c0",
    8: "#8c510a",
    9: "#bf812d",
    10: "#dfc27d",
    11: "#f6e8c3",
    12: "#fde0dd",
    13: "#fa9fb5",
    14: "#c51b8a",
    15: "#7f0000",
    16: "#d9f0a3",
    17: "#addd8e",
    18: "#78c679",
    19: "#2b8cbe",
    20: "#bae4bc",
    21: "#252525",
    22: "#969696",
    23: "#cccccc"
    }

    @action(detail=False, url_path='occupation-du-sol', methods=['get'])
    def get_geospatial_data(self, request):
        # 1. Lire le fichier GeoJSON du polygone
        gdf = gpd.read_file(self.polygone_file)
       # 2. Lire le raster
        try:
            with rasterio.open(self.raster_path) as src:
                # Stocker les métadonnées et les géométries
                profile = src.profile
                raster_crs = src.crs

                # Assurez-vous que le CRS du polygone est le même que celui du raster
                if gdf.crs != raster_crs:
                    gdf = gdf.to_crs(raster_crs)

                # 3. Extraction de la géométrie du polygone pour le masque
                # On utilise .iloc[0] pour prendre la première (et souvent seule) géométrie
                geometries = [gdf.iloc[0].geometry.__geo_interface__]

                # 4. Découpage (Masking) du raster
                out_image, out_transform = mask(src, geometries, crop=True)

                        
                # Le raster découpé a souvent la forme (nombre_de_bandes, hauteur, largeur)

                # 5. Extraction des valeurs de pixels (aplatissement)
                # Supposons un raster à une seule bande (standard pour l'occupation du sol)
                pixel_values = out_image[0].flatten()

                # 6. Ignorer les valeurs de NoData (pixels en dehors du polygone découpé)
                # Par convention, le masque remplit les zones 'NoData' avec la valeur NoData du raster (ou 0)
                # Vous devez connaître la valeur NoData de votre raster d'occupation du sol.
                # Si le raster n'a pas de NoData défini, vous pouvez utiliser la valeur NoData du masque (souvent 0)
                # Attention : si 0 est une classe d'occupation du sol valide, trouvez la vraie valeur NoData.
                # Ici, on suppose que la valeur NoData est 0 ou provient du profil du raster si elle est définie.

                # Trouver la valeur NoData du raster (si définie)
                nodata_val = profile.get('nodata', 0) # Utiliser 0 par défaut si non trouvé

                # Filtrer les valeurs NoData
                valid_pixels = pixel_values[pixel_values != nodata_val]

                # 7. Compter les occurrences de chaque classe de pixel
                counts = pd.Series(valid_pixels).value_counts().sort_index()

                # 8. Calculer le total des pixels valides
                total_pixels = counts.sum()

                # 9. Calculer les proportions
                proportions = (counts / total_pixels) * 100

                # 10. Création du tableau de résultats
                results_df = pd.DataFrame({
                    'ClasseID': counts.index,
                    'ClasseNom': [self.value_to_class.get(i, 'Inconnu') for i in counts.index],
                    'ClasseCouleur': [self.value_to_color.get(i, '#000000') for i in counts.index],
                    'NombrePixels': counts.values,
                    'Proportion': proportions.values
                })
                response = ResponseClass(result=True, has_data=True, message="Données géospatiales extraites avec succès", data=results_df.to_dict(orient='records'))
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=f"Erreur lors de la lecture du raster ou du polygone : {e}")
        finally:
            return response.json_response()
