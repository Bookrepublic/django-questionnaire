from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Count
from django.utils.translation import ugettext_lazy as _


class StatRisposte:
    pass


class Questionnaire(models.Model):
    OPEN = 'open'
    CLOSED = 'closed'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Close'),
    )
    PRIVATE = 'private'
    PUBLIC = 'public'
    PRIVACY_CHOICES = (
        (PRIVATE, 'Private (only logged user)'),
        (PUBLIC, 'Open to everyone'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default=PRIVATE)
    img_banner_home = models.ImageField(upload_to='banner_sondaggio', blank=True, null=True, help_text="Banner che verra' visualizzato in homepage. Per disabilitare selezionare la checkbox 'Cancella' e salvare")

    def __unicode__(self):
        return self.name

    def questions(self):
        return Question.objects.filter(questionset__questionnaire=self)

    def utenti_risposto(self):
        return self.response.all().count()

    @property
    def is_private(self):
        return self.privacy == self.PRIVATE

    @property
    def is_closed(self):
        return self.status == self.CLOSED

    def user_have_already_answered(self, request):
        already_answered = False
        session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]

        q_filter = Q(sessionid=session_key)
        if request.user.is_authenticated():
            q_filter = Q(q_filter|Q(user=request.user))

        answered = Response.objects.filter(q_filter)

        if answered:
            already_answered = True
        return already_answered

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
    heading = models.TextField()

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
    required = models.BooleanField(default=True)

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
    user = models.ForeignKey(User, blank=True, null=True)
    # per gli utenti anonimi salvo la session id
    sessionid = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return ("response %s" % self.user)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response, related_name='answers')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return ("%s. Risposta : %s" % (self.question.text, self.body))
