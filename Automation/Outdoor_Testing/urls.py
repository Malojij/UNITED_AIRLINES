from django.urls import path

from . import views

def outdoor_testing_view(request):
    instance = views.OutdoorTesting()
    return instance.Outdoor_Testing(request)


urlpatterns = [ path('', outdoor_testing_view, name='Outdoor_Testing'),]
