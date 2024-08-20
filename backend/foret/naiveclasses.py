from django.http.response import JsonResponse
class ResponseClass:
    """
    Classe de gestion des réponses HTTP
    :param result: Dis si la réponse positive ``True`` ou négative ``False``
    :param has_data: Dis si la réponse renvoie des données; ``True`` le cas échéant et ``False`` le cas contraire
    :param message: Contient une explication de la réponse
    :param data: Contient les données renvoyés par la réponse. Si ``has_data`` est False, il est None. Dans le cas contraire, il contient les données sérialisées
    """
    def __init__(self, result:bool, has_data:bool, message:str, data=None) -> None:
        self.result = result
        self.has_data = has_data
        self.message = message
        self.data = data
        
    def to_dict(self)->dict:
        return {
            "result":self.result,
            "has_data":self.has_data,
            "message":self.message,
            "data":self.data
        }
    
    def json_response(self):
        return JsonResponse(self.to_dict(), safe=False)