# -*- coding: utf-8 -*-
"""
@author: Kyung-Gyu Park  kgpark88@gmail.com  danny.park@kt.com
"""

from django.urls import include, path
from django.views.generic import TemplateView
from mrc import views

urlpatterns = [
    path('', views.mrc, name='get-answer'),
    path('get-sentence/', views.get_sentence, name='get-sentence'),
    path('get-passage/', views.get_passage, name='get-passage'),
    path('get-question/', views.get_question, name='get-question'),
]
