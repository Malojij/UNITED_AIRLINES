from . import views
from django.urls import path


def api_sequence_view(request):
    instance = views.LogComparor()
    return instance.CompareLog(request)


urlpatterns = [path('', api_sequence_view, name="Log_Comparor"), ]
