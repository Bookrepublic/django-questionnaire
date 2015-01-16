from django.db import models
from django.utils.translation import ugettext_lazy as _


QUESTION_CHOICES = (
    ('free_text', 'Free Text'),
    ('radio_button', 'Radio Button'),
)


class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)

    def __unicode__(self):
        return self.name


class QuestionSet(models.Model):
    """Which questions to display on a question page"""
    questionnaire = models.ForeignKey(Questionnaire)
    ordering = models.IntegerField()
    heading = models.CharField(max_length=64)


class Question(models.Model):
    questionset = models.ForeignKey(QuestionSet)
    text = models.TextField(blank=True, verbose_name=_("Text"))
    type = models.CharField(u"Type of question", max_length=32,
        choices = QUESTION_CHOICES,
        help_text = u"Determines the means of answering the question. " \
        "An open question gives the user a single-line textfield, " \
        "multiple-choice gives the user a number of choices he/she can " \
        "choose from. If a question is multiple-choice, enter the choices " \
        "this user can choose from below'.")


class Choice(models.Model):
    question = models.ForeignKey(Question)
    ordering = models.IntegerField()
    value = models.CharField(u"Short Value", max_length=64)
    text = models.CharField(u"Choice Text", max_length=200)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.number, self.ordering, self.text)
