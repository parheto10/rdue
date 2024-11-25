from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from foret.naiveclasses import ResponseClass

from .importation_controller import ImportationController

class DataImportation(ViewSet):
    
    @action(detail=False, methods=['post'])
    def cadesa(self, request):
        try:
            file = request.data['data']
            campagne = request.data['campagne']
            importation_controller = ImportationController(file, campagne=campagne)
            importation_controller.importer()
            response = ResponseClass(result=True, has_data=True, message=importation_controller.message)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        return response.json_response()