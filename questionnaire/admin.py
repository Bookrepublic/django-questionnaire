from django.contrib import admin
from django.core.urlresolvers import reverse
from questionnaire.models import QuestionSet, Questionnaire, Question, Choice, Response, Answer
from questionnaire.views import QuestionnaireStatistics


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('questionset', 'text', 'question_type', 'ordering')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', '_detail')

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


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'user', 'sessionid')


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionSet)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer)
