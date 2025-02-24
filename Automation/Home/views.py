from django.shortcuts import render
from Response_Builder.Instore_response_builder import Transaction_Processing

def Home(request):
    return render(request, "index.html")
