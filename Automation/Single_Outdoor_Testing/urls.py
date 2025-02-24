from django.urls import path

from . import views

def single_outdoor_testing(request):
    instance = views.Single_Outdoor_Testing()
    return instance.Single_Outdoor_Testing(request)

urlpatterns = [ path('', single_outdoor_testing, name="Single_Outdoor_Testing")]
