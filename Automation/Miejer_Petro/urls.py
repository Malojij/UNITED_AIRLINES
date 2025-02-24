"""Miejer_Petro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home', include('Home.urls')),
    path('', include('Home.urls')),
    path('Instore_Testing', include('Instore_Testing.urls')),
    path('API_SEQUENCE_TESTING', include('API_SEQUENCE_TESTING.urls')),
    path('Ecomm_Testing', include('Ecomm.urls')),
    path('Outdoor_Testing', include('Outdoor_Testing.urls')),
    path('Single_Outdoor_Testing', include('Single_Outdoor_Testing.urls')),
    path('Single_Instore_Testing', include('Single_Instore_Testing.urls')),
    path('Ewic_Testing', include('Ewic_Testing.urls')),
    path('Transaction_Requests', include('Transaction_Requests.urls')),
    path('Other_Scenarios', include('Other_Scenarios.urls')),
    path('DualProcessor', include('DualProcessor.urls')),
    path('Log_Comparor', include('Log_Comparor.urls')),
    path('Aurus_Decryptor', include('Aurus_Decryptor.urls')),
]