from django.urls import path

from .views.search_manager import search_manager

urlpatterns = [
    path('searchmanager/', search_manager, name='register_call'),
]
