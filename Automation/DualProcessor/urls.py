from DualProcessor import views
from django.urls import path

urlpatterns = [
    path('', views.DualProcessor, name="DualProcessor"),
]
