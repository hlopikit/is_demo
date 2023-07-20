from django.urls import path

from .views.demo_data import excel

urlpatterns = [
    path('excel/', excel, name='excel'),
]