from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import Passage, Question


@admin.register(Passage)
class PassageAdmin(ImportExportModelAdmin):
    list_display = ['id', 'no', 'sentence']
    search_fields = ['no', 'sentence']

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'passage', 'no', 'question', 'answer', 's_pos', 'e_pos']
    search_fields = ['question']

