import os
import json
import django

from mrc.models import Sentence, Question

django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# https://github.com/korquad/korquad.github.io/tree/master/dataset
json_file = 'KorQuAD_v1.0_train.json'

json_data = json.load(open(json_file, 'rt', encoding='utf-8'))
version = json_data['version']
data = json_data['data']
for d in data:
    paragraphs = d['paragraphs']
    for p in paragraphs:
        context = p['context']
        qas = p['qas']
        for q in qas:
            qid = q['id']
            sid = qid.split('-')[0]
            question = q['question']
            answers = q['answers']
            answer = answers[0]['text']
            s_pos = answers[0]['answer_start']
            defaults = {'sid':sid, 'qid':qid, 'question': question, 'answer': answer, 's_pos':s_pos}
            Question.objects.update_or_create(qid=qid, defaults=defaults)
        print(f'{sid}')        
        Sentence.objects.update_or_create(sid=sid, defaults={'context':context})



