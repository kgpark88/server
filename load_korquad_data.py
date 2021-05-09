import os
import json
import django

from mrc.models import Passage, Question

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# https://github.com/korquad/korquad.github.io/tree/master/dataset
# json_file = 'KorQuAD_v1.0/KorQuAD_v1.0_dev.json'
json_file = 'KorQuAD_v1.0_train.json'
source = "KorQuAD_v1.0"

json_data = json.load(open(json_file, "rt", encoding="UTF8"))
version = json_data["version"]
data = json_data["data"]
for d in data:
    paragraphs = d['paragraphs']
    for p in paragraphs:
        context = p["context"]
        qas = p['qas']
        p_text = Passage(passage=context, source=source)
        p_text.save()
        print('\n ID {} : CONTEXT : {}'.format(p_text.id, context))
        for q in qas:
            qa_id = q['id']
            question = q['question']
            answers = q['answers']
            text = answers[0]['text']
            answer_start = answers[0]['answer_start']
            defaults = {"passage_id":p_text.id, "question":question, "answer": text, "s_pos": answer_start}
            print(defaults)
            Question.objects.update_or_create(no=qa_id, defaults=defaults)


