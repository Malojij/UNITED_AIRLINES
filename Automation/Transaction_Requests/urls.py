from django.urls import path

from . import views

urlpatterns = [
    path('', views.Transaction_Requests, name="Transaction_Requests"),
]
