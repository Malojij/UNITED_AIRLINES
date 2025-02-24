from django.urls import path
from .consumers import YourConsumer

websocket_urlpatterns = [ path('ws/transactions/', YourConsumer.as_asgi()), ]