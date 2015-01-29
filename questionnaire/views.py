from django.conf import settings
from django.contrib.auth.views import redirect_to_login
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

        if self.questionnaire.is_closed:
            return HttpResponseRedirect(reverse('questionnaire_closed', args=(self.questionnaire.slug,)))

        if self.questionnaire.is_private and not request.user.is_authenticated():
            path = request.META['PATH_INFO']
            return redirect_to_login(path, settings.LOGIN_URL)
        return super(QuestionnaireForm, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.questionnaire = Questionnaire.objects.get(slug=kwargs['slug'])

        if self.questionnaire.is_closed:
            return HttpResponseRedirect(reverse('questionnaire_closed', args=(self.questionnaire.slug,)))

        if self.questionnaire.is_private and not request.user.is_authenticated():
            path = request.META['PATH_INFO']
            return redirect_to_login(path, settings.LOGIN_URL)

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
        # controllo se l'utente ha gia' votato (cercando o un id con la stessa sessione oppure, se e' loggato,
        # delle risposte con quell'utente
        if self.questionnaire.user_have_already_answered(self.request):
            return HttpResponseRedirect(reverse('questionnaire_already_done', args=(self.questionnaire.slug,)))

        # save the response object
        response = Response()
        response.questionnaire = self.questionnaire
        if self.request.user.is_authenticated():
            response.user = self.request.user

        response.sessionid = self.request.COOKIES[settings.SESSION_COOKIE_NAME]
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


class QuestionnaireAlreadyDone(TemplateView):
    template_name = 'questionnaire/questionnaire_already_done.html'


class QuestionnaireClosed(TemplateView):
    template_name = 'questionnaire/questionnaire_closed.html'


class QuestionnaireStatistics(DetailView):
    model = Questionnaire
    template_name = 'questionnaire/admin/questionnaire_statistics.html'