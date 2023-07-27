from django.urls import path

from best_call_manager.views.find_finish_task import find_finish_task
from best_call_manager.views.start_function import start_find_all_call

urlpatterns = [
    path('start_find_all_call/', start_find_all_call,
         name='start_find_all_call'),
    path('finish_find_all_call/', find_finish_task,
         name='find_finish_task'),
]
