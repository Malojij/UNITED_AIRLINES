from django.urls import path

from . import views

urlpatterns = [
    path('', views.Ewic_Testing, name="Ewic_Testing"),
]
