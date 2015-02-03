from cStringIO import StringIO
import csv

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.html import strip_tags
from questionnaire.models import QuestionSet, Questionnaire, Question, Choice, Response, Answer
from questionnaire.views import QuestionnaireStatistics


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('_questionset', '_text', 'question_type', 'ordering')

    def _questionset(self, obj):
        return strip_tags(obj.questionset.heading)

    def _text(self, obj):
        return strip_tags(obj.text)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', '_detail')
    actions = ['answer_csv',]

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urls = super(QuestionnaireAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^(?P<pk>[0-9]+)/statistiche/$',
                               QuestionnaireStatistics.as_view(), {},
                name='questionnaire_statistics'),)
        return my_urls + urls

    def _detail(self, obj):
        return "<a href='%s'>Dettagli</a>" % reverse('admin:questionnaire_statistics', args=(obj.pk,))
    _detail.allow_tags = True

    def answer_csv(self, request, queryset):
        buffer = StringIO()

        columns = ('questionnaire', 'user', 'sessionid', 'question_set', 'question', 'answer')

        writer = csv.DictWriter(buffer, columns, delimiter=';')
        writer.writerow(dict(zip(columns, columns)))
        # for each survey
        for q in queryset:
            # cycle over all the answer
            answer = Answer.objects.filter(response__questionnaire=q)
            for a in answer:
                row = {
                    'questionnaire': q,
                    'user': a.response.user.email.encode('utf-8') if a.response.user and a.response.user.email else '',
                    'sessionid': a.response.sessionid,
                    'question_set': strip_tags(a.question.questionset.heading).encode('utf-8'),
                    'question': strip_tags(a.question.text).encode('utf-8'),
                    'answer': a.body
                }
                writer.writerow(row)
        r = HttpResponse(buffer.getvalue(), mimetype='text/csv')
        r['Content-Disposition'] = 'attachment; filename=survey_answer.csv'
        return r
    answer_csv.short_description = "Export answers in csv"


class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ('ordering', 'questionnaire', '_heading')

    def _heading(self, obj):
        return strip_tags(obj.heading)


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'user', 'sessionid')


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer)
