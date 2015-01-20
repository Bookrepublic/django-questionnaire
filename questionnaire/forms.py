from django import forms
from django.utils.safestring import mark_safe
from questionnaire.models import Question, Questionnaire


# blatantly stolen from
# http://stackoverflow.com/questions/5935546/align-radio-buttons-horizontally-in-django-forms?rq=1
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(slug=kwargs.get('slug'))
        del kwargs['slug']
        super(QuestionForm, self).__init__(*args, **kwargs)

        for q in questionnaire.questions():
            if q.question_type == Question.TEXT:
                self.fields['question_%s' % q.pk] = forms.CharField(label=q.text, widget=forms.Textarea)
            if q.question_type == Question.RADIO:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
                                                                      widget=forms.RadioSelect(
                                                                          renderer=HorizontalRadioRenderer),
                                                                      choices=question_choices)
            self.fields["question_%d" % q.pk].widget.attrs["question_set"] = q.questionset_id