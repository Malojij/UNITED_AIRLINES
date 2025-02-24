from django.urls import path

from . import views

urlpatterns = [
    path('', views.Ecomm_Testing, name="Ecomm_Testing"),
]
