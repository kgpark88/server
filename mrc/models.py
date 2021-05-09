from django.db import models


class Sentence(models.Model):
    sid = models.CharField('문장번호', max_length=10)
    title = models.CharField('문장', max_length=50)
    context = models.TextField('문장')

    class Meta:
        managed = True
        db_table = 'sentence'
        ordering = ['sid']
        verbose_name = '문장'
        verbose_name_plural = '문장'

    def __str__(self):
        return "{} ({})".format(self.sid, self.title)

    def save(self, *args, **kwargs):
        if len(self.context) > 50: 
            title = self.context[0:50].strip()
            if title:
                self.title = title
        super(Sentence, self).save()


class Question(models.Model):
    sid = models.CharField('문장번호', max_length=10)
    qid = models.CharField('질문번호', max_length=15, blank=True, null=True)
    question = models.TextField('질문', max_length=100, blank=True, null=True)
    answer = models.CharField('답', max_length=100, blank=True, null=True)
    s_pos = models.IntegerField('시작위치', blank=True, null=True)
    e_pos = models.IntegerField('종료위치', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'question'
        ordering = ['sid', 'qid']
        verbose_name = '질문'
        verbose_name_plural = '질문'

    def __str__(self):
        return "{} ({})".format(self.sid, self.question)
