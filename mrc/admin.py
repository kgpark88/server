from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import Sentence, Question


@admin.register(Sentence)
class SentenceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sid', 'title', 'context']
    search_fields = ['sid', 'context']

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'sid', 'qid', 'question', 'answer', 's_pos', 'e_pos']
    search_fields = ['sid', 'qid', 'question', 'answer']

