from django.conf.urls.defaults import *
from questionnaire.views import QuestionnaireList, QuestionnaireForm, QuestionnaireThankYou, QuestionnaireStatistics


urlpatterns = patterns('',
    url(r"^$", QuestionnaireList.as_view(), name='questionnaire_list'),
    url(r"^(?P<slug>[-\w]+)/$", QuestionnaireForm.as_view(), name='questionnaire_form'),
    url(r"^(?P<slug>[-\w]+)/thanks/$", QuestionnaireThankYou.as_view(), name='questionnaire_thank_you'),
)
