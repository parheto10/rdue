from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from foret.naiveclasses import ResponseClass

from .importation_controller import ImportationController

import pandas as pd

class DataImportation(ViewSet):
    
    @action(detail=False, methods=['post'])
    def cadesa(self, request):
        try:
            file = request.data['data']
            importation_controller = ImportationController(file)
            nbre_coop = importation_controller.importer()
            response = ResponseClass(result=True, has_data=True, message=f'{nbre_coop} coopérative(s) importée(s)')
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        
        return response.json_response()