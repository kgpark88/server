# -*- coding: utf-8 -*-
"""
@author: Kyung-Gyu Park  kgpark88@gmail.com  danny.park@kt.com
"""
import re
import random
import copy
import json
import logging
import math
import sys
import collections
import os
import unicodedata
import random
import string
import re
import numpy as np


import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn import CrossEntropyLoss, Dropout, Embedding, Softmax
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler, TensorDataset)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from mrc.models import Passage, Question
from mrc.bert_model import Config, BertTokenizer, QuestionAnswering, SquadExample, convert_examples_to_features, RawResult, predictions


def cleanText(readData):
    #텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub("[﻿6-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]", "", readData)
    return text

@api_view(['GET'])
def get_sentence(request):
    '''
    지문 문장 REST API 제공
    ---
    지문 문장 REST API 제공
    '''
    qs = Passage.objects.all().order_by('id')
    sentences = []
    context = {'data': {}}
    for q in qs:
        db_data = {
          'id': q.id,
          'no': q.no or '',
          'sentence': q.sentence or '',
          'passage': q.passage or '',
          'source': q.source or ''
        }
        sentences.append(q.sentence)
    print(f'GET Passage Title : {len(sentences)}건')
    context = {'sentences': sentences}
    return JsonResponse(context)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='문장'),
    }
))
@api_view(['POST'])
def get_passage(request):
    '''
    문장 REST API 제공
    ---
    문장 REST API 제공
    '''
    title = request.data['title'].strip()
    qs1 = Passage.objects.filter(sentence=title)

    qas = []
    qs2 = Question.objects.filter(passage__id=qs1[0].id).order_by('no')
    for q in qs2:
        qas.append({"question": q.question, "answer": q.answer})

    context = {'passage': qs1[0].passage, 'qas': qas}

    print(qs1[0].id)
    print(context)
    return JsonResponse(context)



@api_view(['POST'])
def get_question(request):
    '''
    문장에 관련된 질문 REST API 제공
    ---
    문장에 관련된 질문문장 REST API 제공
    '''
    passage_id = int(request.data['passage_id'])
    question = []
    qs = Question.objects.filter(passage__id=passage_id)
    for q in qs:
        question.append(q.question)
    random.shuffle(question)
    # print(f'[Passage ID] : {passage_id}')
    # print(f'[Question] : {question}')
    context = {'question': question}
    return JsonResponse(context)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'passage': openapi.Schema(type=openapi.TYPE_STRING, description='문장'),
        'question': openapi.Schema(type=openapi.TYPE_STRING, description='질문'),
    }
))
@api_view(['POST'])
def mrc(request):
    '''
    기계독해 REST API 제공
    ---
    기계독해 REST API 제공
    '''
    qas_id = '1234567-0-0'
    passage = request.data['passage']
    question = request.data['question'].strip()

    max_seq_length = 512
    doc_stride = 128
    max_query_length = 96
    max_answer_length = 30
    n_best_size = 20

    model_dir = "bert_small"
    model_config = os.path.join(model_dir, "bert_small.json")
    vocab_file = os.path.join(model_dir, "ko_vocab_32k.txt")
    tokenizer = BertTokenizer(vocab_file, max_len=max_seq_length, do_basic_tokenize=True)

    config = Config.from_json_file(model_config)
    checkpoint = os.path.join(model_dir, "korquad_9.bin")

    device = torch.device('cpu')
    model = QuestionAnswering(config)
    model.load_state_dict(torch.load(checkpoint, map_location=device) )
    model.eval()


    start_position = -1
    end_position = -1
    orig_answer_text = ""
    is_impossible = True

    eval_examples = [SquadExample(
                        qas_id=qas_id,
                        question_text=question,
                        doc_tokens=[passage],
                        orig_answer_text=orig_answer_text,
                        start_position=start_position,
                        end_position=end_position,
                        is_impossible=is_impossible)]

    eval_features = convert_examples_to_features(examples=eval_examples,
                                            tokenizer=tokenizer,
                                            max_seq_length=max_seq_length,
                                            doc_stride=doc_stride,
                                            max_query_length=max_query_length,
                                            is_training=False)

    input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)


    batch_start_logits, batch_end_logits = model(input_ids, segment_ids, input_mask)

    start_logits = batch_start_logits[0].detach().cpu().tolist()
    end_logits = batch_end_logits[0].detach().cpu().tolist()
    eval_feature = eval_features[0]
    unique_id = int(eval_feature.unique_id)
    result = RawResult(unique_id=unique_id,
                    start_logits=start_logits,
                    end_logits=end_logits)
        
    pred, probability, nbest_json  = predictions(eval_examples, eval_features, [result], n_best_size, 
                      max_answer_length, False, False, 
                      False, 0.0)
    answer = list(pred.values())[0]
    start_index = passage.find(answer)
    end_index = start_index +len(answer)

    no_answer = ['잘 모르겠어요.', '좀 더 공부할께요.', '저도 궁금하네요.', '음...', '뭘까요?']
    if len(answer) > 100:
        answer = random.choice(no_answer)
        probability = 0
        start_index = 0
        end_index = 0

    context = {'answer': answer, 'start_index': start_index, 'end_index': end_index, 'probability':probability }
    return JsonResponse(context)


