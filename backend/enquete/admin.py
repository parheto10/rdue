from django.contrib import admin

from .models import TypeEnquete, Enquete, TypeQuestion, Question, Reponse, Enqueteur, Condition

admin.site.register(TypeEnquete)
admin.site.register(Enquete)
admin.site.register(TypeQuestion)
admin.site.register(Question)
admin.site.register(Reponse)
admin.site.register(Enqueteur)
admin.site.register(Condition)