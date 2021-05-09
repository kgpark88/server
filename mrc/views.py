import os
import torch

from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from mrc.models import Sentence, Question

from mrc.bert_model import Config, BertTokenizer, QuestionAnswering, SquadExample 
from mrc.bert_model import convert_examples_to_features, RawResult, predictions

from transformers import ElectraTokenizer, ElectraForQuestionAnswering, pipeline

def cleanText(readData):
    text = re.sub("[﻿6-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]", "", readData)
    return text

@api_view(['GET'])
def titles(request):
    qs = Sentence.objects.all().order_by('id')[:200]
    titles = []
    for q in qs:
        titles.append({'sid': q.sid, 'title': q.title})
    return JsonResponse({'titles':titles})

@api_view(['POST'])
def sentence(request):
    sid = request.data.get('sid')
    sentence = Sentence.objects.filter(sid=sid)
    if sentence:
        qas = []
        question = Question.objects.filter(sid=sid).order_by('qid')
        for q in question:
            qas.append({"question": q.question, "answer": q.answer})
        res = {'sentence': sentence[0].context, 'qas': qas}
    else:
        res = {'sentence': None, 'qas': None}
    return JsonResponse(res)

@api_view(['POST'])
def question(request):
    qid = int(request.data.get('qid'))
    question = []
    qs = Question.objects.filter(qid=qid)
    for q in qs:
        question.append(q.question)
    random.shuffle(question)
    res = {'question': question}
    return JsonResponse(res)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'passage': openapi.Schema(type=openapi.TYPE_STRING, description='문장'),
        'question': openapi.Schema(type=openapi.TYPE_STRING, description='질문'),
    }
))
@api_view(['POST'])
def question_answer(request):
    '''
    기계독해 REST API 제공
    ---
    기계독해 REST API 제공
    '''
    qas_id = '1234567-0-0'
    sentence = request.data['sentence']
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
                        doc_tokens=[sentence],
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
    start_index = sentence.find(answer)
    end_index = start_index +len(answer)

    no_answer = ['잘 모르겠어요.', '좀 더 공부할께요.', '저도 궁금하네요.', '음...', '뭘까요?']
    if len(answer) > 100:
        answer = random.choice(no_answer)
        probability = 0
        start_index = 0
        end_index = 0

    context = {'answer': answer, 'start': start_index, 'end': end_index, 'score':probability }
    return JsonResponse(context)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'passage': openapi.Schema(type=openapi.TYPE_STRING, description='문장'),
        'question': openapi.Schema(type=openapi.TYPE_STRING, description='질문'),
    }
))
@api_view(['POST'])
def question_answer_pipeline(request):
    '''
    Question Answering REST API
    '''
    sentence = request.data['sentence'].strip()
    question = request.data['question'].strip()

    tokenizer = ElectraTokenizer.from_pretrained('monologg/koelectra-base-v2-finetuned-korquad')
    model = ElectraForQuestionAnswering.from_pretrained('monologg/koelectra-base-v2-finetuned-korquad')

    qa = pipeline('question-answering', tokenizer=tokenizer, model=model)
    ans = qa({'context': sentence, 'question': question})
    res = {
        'answer': ans['answer'], 
        'start': ans['start'], 
        'end': ans['end'], 
        'score':ans['score'] 
    }
    print(res)
    return JsonResponse(res)
