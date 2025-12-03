from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from foret.naiveclasses import ResponseClass

from .importation_controller import ImportationController

class DataImportation(ViewSet):
    
    @action(detail=False, methods=['post'])
    def planting(self, request):
        try:
            file = request.data['data']
            campagne = request.data['campagne']
            sheet_number = request.data.get('sheet_number', 0)
            importation_controller = ImportationController(file, campagne=campagne, sheet_number=sheet_number)
            importation_controller.importer()
            response = ResponseClass(result=True, has_data=True, message=importation_controller.message)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e), data=importation_controller.stats if 'importation_controller' in locals() else {})
        return response.json_response()
    
    @action(detail=False, methods=['post'])
    def monitoring(self, request):
        try:
            file = request.data['data']
            campagne = request.data['campagne']
            importation_controller = ImportationController(file, campagne=campagne)
            importation_controller.importation_monitoring()
            response = ResponseClass(result=True, has_data=True, message=importation_controller.message)
        except Exception as e:
            response = ResponseClass(result=False, has_data=False, message=str(e))
        return response.json_response()