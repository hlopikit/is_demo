from django.urls import path
from .views.complete_tasks import finish_tasks, initiate_completion
from .views.set_flag import set_flag

urlpatterns = [
    # path('complete_tasks/', complete_tasks, name='complete_tasks'),
    path('complete_tasks/', initiate_completion, name='complete_tasks'),
    path('set_flag/', set_flag, name='set_flag'),
]