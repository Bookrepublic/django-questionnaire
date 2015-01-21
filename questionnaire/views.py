from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView, TemplateView, DetailView
from questionnaire.forms import QuestionForm
from questionnaire.models import Questionnaire, Response, Question, Answer


class QuestionnaireList(ListView):
    model = Questionnaire
    template_name = 'questionnaire/questionnaire_list.html'


class QuestionnaireForm(FormView):
    template_name = 'questionnaire/questionnaire_form.html'
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.questionnaire = Questionnaire.objects.get(slug=kwargs['slug'])
        return super(QuestionnaireForm, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.questionnaire = Questionnaire.objects.get(slug=kwargs['slug'])
        return super(QuestionnaireForm, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(QuestionnaireForm, self).get_form_kwargs()
        kwargs['slug'] = self.kwargs['slug']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireForm, self).get_context_data(**kwargs)
        context['question_set'] = self.questionnaire.question_set.all()
        return context

    def form_valid(self, form):
        # save the response object
        response = Response()
        response.questionnaire = self.questionnaire
        response.user = self.request.user
        response.save()

        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in form.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in the
                # field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                q = Question.objects.get(pk=q_id)

                a = Answer()
                a.question = q
                a.response = response
                a.body = field_value
                a.save()

        return HttpResponseRedirect(reverse('questionnaire_thank_you', args=(self.questionnaire.slug,)))


class QuestionnaireThankYou(TemplateView):
    template_name = 'questionnaire/questionnaire_thank_you.html'


class QuestionnaireStatistics(DetailView):
    model = Questionnaire
    template_name = 'questionnaire/admin/questionnaire_statistics.html'