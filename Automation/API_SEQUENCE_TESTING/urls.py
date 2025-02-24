from . import views
from django.urls import path


def api_sequence_view(request):
    instance = views.ISSUE_SEQUENCE_TESTING()
    return instance.issue_sequence_testing(request)


urlpatterns = [path('', api_sequence_view, name="API_SEQUENCE_TESTING"), ]
