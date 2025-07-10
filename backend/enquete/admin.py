from django.contrib import admin

from .models import TypeEnquete, Enquete, TypeQuestion, Question, Reponse, Enqueteur

from import_export.admin import ImportExportModelAdmin

class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'libelle', 'est_obligatoire', 'type_question', 'enquete']
    list_filter = ['enquete__identifiant', 'type_question__libelle']
    search_fields = ['libelle', 'enquete__identifiant']

class ReponseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'enquete', 'repondant', 'submitted_at']
    list_filter = ['enquete__identifiant', 'repondant__nom']
    search_fields = ['enquete__identifiant', 'repondant__nom']

admin.site.register(TypeEnquete, ImportExportModelAdmin)
admin.site.register(Enquete, ImportExportModelAdmin)
admin.site.register(TypeQuestion, ImportExportModelAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Reponse, ReponseAdmin)
admin.site.register(Enqueteur, ImportExportModelAdmin)