from django.contrib import admin
from questionnaire.models import QuestionSet, Questionnaire, Question, Choice, Response, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Questionnaire)
admin.site.register(QuestionSet)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(Answer)
