# -*- coding: utf-8 -*-
"""
@author: Kyung-Gyu Park  kgpark88@gmail.com  danny.park@kt.com
"""

from django.urls import include, path
from django.views.generic import TemplateView
from mrc import views

urlpatterns = [
    path('qa', views.question_answer, name='qa'),
    path('qa-pipeline', views.question_answer_pipeline, name='qa-pipeline'),
    path('titles', views.titles, name='titles'),
    path('sentence', views.sentence, name='sentence'),
    path('question', views.question, name='question'),
]
