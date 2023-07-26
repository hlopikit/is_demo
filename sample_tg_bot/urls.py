from django.urls import path

from .views.send_message import send_message

urlpatterns = [
    path('send_message/', send_message, name='send_message'),
]
