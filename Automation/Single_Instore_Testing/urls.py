from django.urls import path
from . import views

def Single_Instore_Testing(request):
    instance = views.Single_Instore_Testing()
    return instance.Single_Instore_Testing(request)


urlpatterns = [path('', Single_Instore_Testing, name="Single_Instore_Testing")]
