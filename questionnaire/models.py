from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _


class StatRisposte:
    pass


class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)

    def __unicode__(self):
        return self.name

    def questions(self):
        return Question.objects.filter(questionset__questionnaire=self)

    def utenti_risposto(self):
        return self.response.all().count()

    def statistiche_risposte(self):
        d_answer = {}
        answer_agg = Answer.objects.filter(response__questionnaire=1).values('question', 'body').annotate(risposte=Count('body'))
        for a in answer_agg:
            d_answer[(a['question'], a['body'])] = a['risposte']

        stat_risp = []
        for q_set in self.question_set.all():
            sr = StatRisposte()
            sr.heading = q_set.heading
            sr.questions = []
            for q in q_set.questions.all():
                sq = StatRisposte()
                sq.domanda = q.text
                sq.choices = []
                for c in q.choices.all():
                    num_risposte = d_answer.get((q.pk, c.text), 0)
                    sq.choices.append([c, num_risposte])
                sr.questions.append(sq)
            stat_risp.append(sr)
        return stat_risp


class QuestionSet(models.Model):
    """Which questions to display on a question page"""
    questionnaire = models.ForeignKey(Questionnaire, related_name='question_set')
    ordering = models.IntegerField()
    heading = models.CharField(max_length=250)

    def __unicode__(self):
        return u"%s" % (self.heading,)

    class Meta:
        ordering = ('ordering',)


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_CHOICES = (
        (TEXT, 'Text'),
        (RADIO, 'Radio Button'),
    )

    questionset = models.ForeignKey(QuestionSet, related_name='questions')
    ordering = models.IntegerField()
    text = models.TextField(blank=True, verbose_name=_("Text"))
    question_type = models.CharField(u"Type of question", max_length=32,
        choices = QUESTION_CHOICES,
        help_text = u"Determines the means of answering the question. " \
        "An open question gives the user a single-line textfield, " \
        "multiple-choice gives the user a number of choices he/she can " \
        "choose from. If a question is multiple-choice, enter the choices " \
        "this user can choose from below'.")

    def get_choices(self):
        """parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget."""
        choices_list = []
        for c in self.choices.all():
            choices_list.append((c.value, c.text))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return u"%s - %s" % (self.questionset, self.text)

    class Meta:
        ordering = ('ordering',)


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    ordering = models.IntegerField()
    value = models.CharField(u"Short Value", max_length=64)
    text = models.CharField(u"Choice Text", max_length=200)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question, self.ordering, self.text)

    class Meta:
        ordering = ('ordering',)


class Response(models.Model):
    # a response object is just a collection of questions and answers with a
    # unique interview uuid
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='response')
    user = models.ForeignKey(User)

    def __unicode__(self):
        return ("response %s" % self.user)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return ("%s. Risposta : %s" % (self.question.text, self.body))
