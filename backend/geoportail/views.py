from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from foret.naiveclasses import ResponseClass
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import pandas as pd
import numpy as np
import json

class GeoportailViewSet(ViewSet):
    raster_path = str(settings.GEODATA_ROOT) + '/ocs2020.tif'
    polygone_file = str(settings.GEODATA_ROOT) + '/polygon.geojson'

    def _convert_to_json_serializable(self, obj):
        """
        Convertit les objets numpy et pandas en types Python natifs sérialisables en JSON
        """
        if isinstance(obj, dict):
            return {key: self._convert_to_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._convert_to_json_serializable(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        else:
            return obj
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
                response = ResponseClass(result=True, has_data=True, message="Données géospatiales extraites avec succès", data=self._convert_to_json_serializable(results_df.to_dict(orient='records')))
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=f"Erreur lors de la lecture du raster ou du polygone : {e}")
        finally:
            return response.json_response()

    @action(detail=False, url_path='occupation-du-sol-parcelle', methods=['get'])
    def get_geospatial_data_by_property(self, request):
        """
        Traite un polygone sélectionné par la valeur d'une propriété depuis un fichier GeoJSON.
        Paramètres de requête:
        - file: nom du fichier GeoJSON (défaut: capressa.geojson)
        - property: nom de la propriété à utiliser pour le filtrage (ex: CODE, NOM, VILLAGE)
        - value: valeur de la propriété à rechercher
        """
        try:
            # Paramètres de requête
            filename = 'capressa.geojson'
            property_value = request.query_params.get('code_parcelle')

            if property_value is None:
                return ResponseClass(result=False, has_data=False,
                                   message="Le paramètre 'code_parcelle' est requis").json_response()
            geojson_path = str(settings.GEODATA_ROOT) + f'/{filename}'

            # Vérifier que le fichier existe
            import os
            if not os.path.exists(geojson_path):
                return ResponseClass(result=False, has_data=False,
                                   message=f"Fichier GeoJSON non trouvé: {filename}").json_response()

            # Lire le fichier GeoJSON
            gdf = gpd.read_file(geojson_path)

            # Filtrer par la propriété et valeur spécifiées
            # Essayer d'abord une correspondance exacte
            filtered_gdf = gdf[gdf['CODE'] == str(property_value)]

            # Vérifier qu'on a trouvé au moins un résultat
            if len(filtered_gdf) == 0:
                return ResponseClass(result=False, has_data=False,
                                   message=f"Aucun polygone trouvé avec CODE = '{property_value}'").json_response()

            # Si plusieurs résultats, prendre le premier et avertir
            if len(filtered_gdf) > 1:
                selected_row = filtered_gdf.iloc[0]
                warning_message = f"Plusieurs polygones ({len(filtered_gdf)}) trouvés avec CODE = '{property_value}'. Utilisation du premier résultat."
            else:
                selected_row = filtered_gdf.iloc[0]
                warning_message = None

            # Obtenir l'index original dans le GeoDataFrame complet
            original_index = gdf.index.get_loc(selected_row.name)
            selected_geometry = selected_row.geometry

            # Lire le raster
            with rasterio.open(self.raster_path) as src:
                profile = src.profile
                raster_crs = src.crs

                # Assurer la cohérence des CRS
                if gdf.crs != raster_crs:
                    # Créer un GeoDataFrame temporaire avec le polygone sélectionné
                    temp_gdf = gpd.GeoDataFrame([selected_row], geometry=[selected_geometry], crs=gdf.crs)
                    temp_gdf = temp_gdf.to_crs(raster_crs)
                    selected_geometry = temp_gdf.iloc[0].geometry

                # Préparer la géométrie pour le masque
                geometries = [selected_geometry.__geo_interface__]

                # Découpage du raster
                out_image, out_transform = mask(src, geometries, crop=True)
                pixel_values = out_image[0].flatten()

                # Gestion des valeurs NoData
                nodata_val = profile.get('nodata', 0)
                valid_pixels = pixel_values[pixel_values != nodata_val]

                if len(valid_pixels) == 0:
                    response_data = {
                        'polygon_index': original_index,
                        'properties': self._convert_to_json_serializable(dict(selected_row.drop('geometry'))),
                        'statistics': {
                            'total_pixels': 0,
                            'classes': [],
                            'message': 'Aucun pixel valide trouvé pour ce polygone'
                        }
                    }
                    if warning_message:
                        response_data['warning'] = warning_message
                    return ResponseClass(result=True, has_data=True,
                                       message="Aucun pixel valide trouvé", data=response_data).json_response()

                # Comptage des classes
                counts = pd.Series(valid_pixels).value_counts().sort_index()
                total_pixels = counts.sum()
                proportions = (counts / total_pixels) * 100

                # Création des résultats
                classes_data = []
                for class_id, count in counts.items():
                    classes_data.append({
                        'ClasseID': int(class_id),
                        'ClasseNom': self.value_to_class.get(int(class_id), 'Inconnu'),
                        'ClasseCouleur': self.value_to_color.get(int(class_id), '#000000'),
                        'NombrePixels': int(count),
                        'Proportion': float(proportions[class_id])
                    })

                response_data = {
                   
                    'polygon_index': original_index,
                    'properties': self._convert_to_json_serializable(dict(selected_row.drop('geometry'))),
                    'statistics': {
                        'total_pixels': int(total_pixels),
                        'classes': classes_data
                    }
                }

                if warning_message:
                    response_data['warning'] = warning_message
    
                message = "Statistiques du polygone extraites avec succès"
                if warning_message:
                    message += " (avec avertissement)"

                return ResponseClass(result=True, has_data=True,
                                   message=message, data=classes_data).json_response()

        except Exception as e:
            return ResponseClass(result=False, has_data=False,
                               message=f"Erreur lors du traitement : {e}").json_response()

    @action(detail=False, url_path='proprietes-geojson', methods=['get'])
    def get_geojson_properties(self, request):
        """
        Liste les propriétés disponibles dans un fichier GeoJSON et leurs valeurs uniques.
        Paramètres de requête:
        - file: nom du fichier GeoJSON (défaut: capressa.geojson)
        - property: nom d'une propriété spécifique pour voir ses valeurs uniques (optionnel)
        """
        try:
            # Paramètres de requête
            filename = request.query_params.get('file', 'capressa.geojson')
            specific_property = request.query_params.get('property')

            geojson_path = str(settings.GEODATA_ROOT) + f'/{filename}'

            # Vérifier que le fichier existe
            import os
            if not os.path.exists(geojson_path):
                return ResponseClass(result=False, has_data=False,
                                   message=f"Fichier GeoJSON non trouvé: {filename}").json_response()

            # Lire le fichier GeoJSON
            gdf = gpd.read_file(geojson_path)

            # Obtenir les colonnes (exclure geometry)
            columns = [col for col in gdf.columns if col != 'geometry']

            if specific_property:
                # Vérifier que la propriété existe
                if specific_property not in columns:
                    return ResponseClass(result=False, has_data=False,
                                       message=f"Propriété '{specific_property}' introuvable. Propriétés disponibles: {', '.join(columns)}").json_response()

                # Obtenir les valeurs uniques pour cette propriété
                unique_values = gdf[specific_property].unique()
                # Convertir en liste et gérer les types
                values_list = []
                for val in unique_values:
                    if pd.isna(val):
                        values_list.append(None)
                    else:
                        values_list.append(str(val))

                response_data = {
                    'file': filename,
                    'property': specific_property,
                    'unique_values_count': len(values_list),
                    'unique_values': sorted(values_list, key=lambda x: (x is None, x))
                }
            else:
                # Lister toutes les propriétés avec des informations
                properties_info = []
                for col in columns:
                    unique_count = gdf[col].nunique()
                    has_nulls = gdf[col].isnull().any()
                    sample_values = gdf[col].dropna().unique()[:5]  # 5 premiers exemples

                    properties_info.append({
                        'name': col,
                        'unique_values_count': int(unique_count),
                        'has_null_values': bool(has_nulls),
                        'sample_values': [str(val) for val in sample_values],
                        'data_type': str(gdf[col].dtype)
                    })

                response_data = {
                    'file': filename,
                    'total_features': len(gdf),
                    'properties_count': len(columns),
                    'properties': properties_info
                }

            return ResponseClass(result=True, has_data=True,
                               message="Propriétés GeoJSON récupérées avec succès",
                               data=response_data).json_response()

        except Exception as e:
            return ResponseClass(result=False, has_data=False,
                               message=f"Erreur lors de la récupération des propriétés : {e}").json_response()
