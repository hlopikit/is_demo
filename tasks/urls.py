from django.urls import path

from tasks.views.get_fact import get_fact

urlpatterns = [
    path('get_fact/', get_fact),
]
