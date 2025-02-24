from Aurus_Decryptor import views
from django.urls import path


def Decryptor_view(request):
    instance = views.Aurus_Decryptor()
    return instance.Decryptor(request)


urlpatterns = [ path('', Decryptor_view, name='Aurus_Decryptor'),]