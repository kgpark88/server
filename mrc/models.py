from django.db import models

class TimeStampedModel(models.Model):
    created = models.DateTimeField('생성일시', auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField('수정일시', auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Passage(TimeStampedModel):
    no = models.CharField('번호', max_length=15, blank=True, null=True)
    sentence = models.CharField('문장', max_length=100, blank=True, null=True)
    passage = models.TextField()
    topic = models.CharField('토픽', max_length=100, blank=True, null=True)
    category = models.CharField('카테고리', max_length=50, blank=True, null=True)    
    source = models.CharField('출처', max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mrc_passage'
        ordering = ['id']
        verbose_name = '문장'
        verbose_name_plural = '문장'

    def __str__(self):
        return "{} ({})".format(self.no, self.sentence)

    def save(self, *args, **kwargs):
        self.no = self.id 
        if len(self.passage) > 50: 
            sentence = self.passage[0:50].strip()
            self.sentence = sentence
        super(Passage, self).save()


class Question(TimeStampedModel):
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    no = models.CharField('번호', max_length=15, blank=True, null=True)
    question = models.TextField('질문', max_length=100, blank=True, null=True)
    answer = models.CharField('답', max_length=100, blank=True, null=True)
    s_pos = models.IntegerField('시작위치', blank=True, null=True)
    e_pos = models.IntegerField('종료위치', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mrc_question'
        ordering = ['passage__no', 'no']
        verbose_name = '질문'
        verbose_name_plural = '질문'

    def __str__(self):
        return "{} ({})".format(self.no, self.question)
