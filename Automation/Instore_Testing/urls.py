from Instore_Testing import views
from django.urls import path


def instore_testing_view(request):
    instance = views.InstoreTesting()
    return instance.Instore_Testing(request)


urlpatterns = [ path('', instore_testing_view, name='Instore_Testing'),]