from django.urls import path

from best_call_manager.views.start_function import start_find_all_call

urlpatterns = [
    path('start_find_all_call/', start_find_all_call,
         name='start_find_all_call'),
]
